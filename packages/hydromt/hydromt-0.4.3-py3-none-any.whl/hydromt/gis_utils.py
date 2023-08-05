#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""gis related convience functions. More in pyflwdir.gis_utils"""
from os.path import join, isfile
import numpy as np
import xarray as xr
import rasterio
from rasterio.crs import CRS
from rasterio.transform import Affine
from osgeo import gdal
import geopandas as gpd
from shapely.geometry.base import BaseGeometry
from shapely.geometry import box
import tempfile
from pyflwdir import core_conversion, core_d8, core_ldd

_R = 6371e3  # Radius of earth in m. Use 3956e3 for miles
XATTRS = {
    "geographic": {
        "standard_name": "longitude",
        "long_name": "longitude coordinate",
        "short_name": "lon",
        "units": "degrees_east",
    },
    "projected": {
        "standard_name": "projection_x_coordinate",
        "long_name": "x coordinate of projection",
        "short_name": "x",
        "units": "m",
    },
}
YATTRS = {
    "geographic": {
        "standard_name": "latitude",
        "long_name": "latitude coordinate",
        "short_name": "lat",
        "units": "degrees_north",
    },
    "projected": {
        "standard_name": "projection_y_coordinate",
        "long_name": "y coordinate of projection",
        "short_name": "y",
        "units": "m",
    },
}
PCR_VS_MAP = {"ldd": "ldd"}
GDAL_DRIVER_CODE_MAP = {
    "asc": "AAIGrid",
    "blx": "BLX",
    "bmp": "BMP",
    "bt": "BT",
    "dat": "ZMap",
    "dem": "USGSDEM",
    "gen": "ADRG",
    "gif": "GIF",
    "gpkg": "GPKG",
    "grd": "NWT_GRD",
    "gsb": "NTv2",
    "gtx": "GTX",
    "hdr": "MFF",
    "hf2": "HF2",
    "hgt": "SRTMHGT",
    "img": "HFA",
    "jpg": "JPEG",
    "kro": "KRO",
    "lcp": "LCP",
    "map": "PCRaster",
    "mbtiles": "MBTiles",
    "mpr/mpl": "ILWIS",
    "ntf": "NITF",
    "pix": "PCIDSK",
    "png": "PNG",
    "pnm": "PNM",
    "rda": "R",
    "rgb": "SGI",
    "rst": "RST",
    "rsw": "RMF",
    "sdat": "SAGA",
    "sqlite": "Rasterlite",
    "ter": "Terragen",
    "tif": "GTiff",
    "vrt": "VRT",
    "xpm": "XPM",
    "xyz": "XYZ",
}
GDAL_EXT_CODE_MAP = {v: k for k, v in GDAL_DRIVER_CODE_MAP.items()}

##


def filter_gdf(gdf, geom=None, bbox=None, predicate="intersects"):
    """Filter GeoDataFrame geometries based on geometry mask or bounding box."""
    gtypes = (gpd.GeoDataFrame, gpd.GeoSeries, BaseGeometry)
    if bbox is not None and geom is None:
        geom = box(*bbox)
    elif geom is not None and not isinstance(geom, gtypes):
        raise ValueError(
            f"Unknown geometry mask type {type(geom).__name__}. "
            "Provide geopandas GeoDataFrame, GeoSeries or shapely geometry."
        )
    elif bbox is None and geom is None:
        raise ValueError("Either geom or bbox is required.")
    if not isinstance(geom, BaseGeometry):
        # reproject
        if gdf.crs is not None and geom.crs != gdf.crs:
            geom = geom.to_crs(gdf.crs)
        # convert geopandas to geometry
        geom = geom.unary_union
    idx = gdf.sindex.query(geom, predicate=predicate)
    return idx


# REPROJ
def utm_crs(bbox):
    """Returns wkt string of nearest UTM projects

    Parameters
    ----------
    bbox : array-like of floats
        (xmin, ymin, xmax, ymax) bounding box in latlon WGS84 (EPSG:4326) coordinates

    Returns
    -------
    crs: pyproj.CRS
        CRS of UTM projection
    """
    left, bottom, right, top = bbox
    x = (left + right) / 2
    y = (top + bottom) / 2
    kwargs = dict(zone=int(np.ceil((x + 180) / 6)))
    # BUGFIX hydroMT v0.3.5: south=False doesn't work only add south=True if y<0
    if y < 0:
        kwargs.update(south=True)
    epsg = CRS(proj="utm", ellps="WGS84", **kwargs).to_epsg()
    return CRS.from_epsg(epsg)


def parse_crs(crs, bbox=None):
    if crs == "utm":
        if bbox is not None:
            crs = utm_crs(bbox)
        else:
            raise ValueError('CRS "utm" requires bbox')
    else:
        crs = CRS.from_user_input(crs)
    return crs


def axes_attrs(crs):
    """
    Provide CF-compliant variable names and metadata for axes

    Parameters
    ----------
    crs: pyproj.CRS
        coordinate reference system

    Returns
    -------
    x_dim: str - variable name of x dimension (e.g. 'x')
    y_dim: str - variable name of y dimension (e.g. 'lat')
    x_attr: dict - attributes of variable x
    y_attr: dict - attributes of variable y
    """
    # check for type of crs
    crs_type = "geographic" if crs.is_geographic else "projected"
    y_dim = YATTRS[crs_type]["short_name"]
    x_dim = XATTRS[crs_type]["short_name"]
    y_attrs = YATTRS[crs_type]
    x_attrs = XATTRS[crs_type]
    return x_dim, y_dim, x_attrs, y_attrs


def meridian_offset(ds, x_name, bbox=None):
    """re-arange data along x dim"""
    lons = np.copy(ds[x_name].values)
    w, e = lons.min(), lons.max()
    if bbox is not None and bbox[0] < w and bbox[0] < -180:  # 180W - 180E > 360W - 0W
        lons = np.where(lons > bbox[2], lons - 360, lons)
    elif bbox is not None and bbox[2] > e and bbox[2] > 180:  # 180W - 180E > 0E-360E
        lons = np.where(lons < bbox[0], lons + 360, lons)
    elif e > 180:  # 0E-360E > 180W - 180E
        lons = np.where(lons > 180, lons - 360, lons)
    else:
        return ds
    ds[x_name] = xr.Variable(ds[x_name].dims, lons)
    return ds


# TRANSFORM


def affine_to_coords(transform, shape):
    """Returs a raster axis with pixel center coordinates based on the transform.

    Parameters
    ----------
    transform : affine transform
        Two dimensional affine transform for 2D linear mapping
    shape : tuple of int
        The height, width  of the raster.

    Returns
    -------
    x, y coordinate arrays : tuple of ndarray of float
    """
    if not isinstance(transform, Affine):
        transform = Affine(*transform)
    height, width = shape
    x_coords, _ = transform * (np.arange(width) + 0.5, np.zeros(width) + 0.5)
    _, y_coords = transform * (np.zeros(height) + 0.5, np.arange(height) + 0.5)
    return x_coords, y_coords


## CELLAREAS
def reggrid_area(lats, lons):
    """Returns the cell area [m2] for a regular grid based on its cell centres
    lat, lon coordinates."""
    xres = np.abs(np.mean(np.diff(lons)))
    yres = np.abs(np.mean(np.diff(lats)))
    area = np.ones((lats.size, lons.size), dtype=lats.dtype)
    return cellarea(lats, xres, yres)[:, None] * area


def cellarea(lat, xres=1.0, yres=1.0):
    """Return the area [m2] of cell based on the cell center latitude and its resolution
    in measured in degrees."""
    l1 = np.radians(lat - np.abs(yres) / 2.0)
    l2 = np.radians(lat + np.abs(yres) / 2.0)
    dx = np.radians(np.abs(xres))
    return _R ** 2 * dx * (np.sin(l2) - np.sin(l1))


def cellres(lat, xres=1.0, yres=1.0):
    """Return the cell (x, y) resolution [m] based on cell center latitude and its
    resolution measured in degrees."""
    m1 = 111132.92  # latitude calculation term 1
    m2 = -559.82  # latitude calculation term 2
    m3 = 1.175  # latitude calculation term 3
    m4 = -0.0023  # latitude calculation term 4
    p1 = 111412.84  # longitude calculation term 1
    p2 = -93.5  # longitude calculation term 2
    p3 = 0.118  # longitude calculation term 3

    radlat = np.radians(lat)  # numpy cos work in radians!
    # Calculate the length of a degree of latitude and longitude in meters
    dy = (
        m1
        + (m2 * np.cos(2.0 * radlat))
        + (m3 * np.cos(4.0 * radlat))
        + (m4 * np.cos(6.0 * radlat))
    )
    dx = (
        (p1 * np.cos(radlat))
        + (p2 * np.cos(3.0 * radlat))
        + (p3 * np.cos(5.0 * radlat))
    )

    return dx * xres, dy * yres


## PCRASTER


def write_clone(tmpdir, gdal_transform, wkt_projection, shape):
    """write pcraster clone file to a tmpdir using gdal"""
    gdal.AllRegister()
    driver1 = gdal.GetDriverByName("GTiff")
    driver2 = gdal.GetDriverByName("PCRaster")
    fn = join(tmpdir, "clone.map")
    # create temp tif file
    fn_temp = join(tmpdir, "clone.tif")
    TempDataset = driver1.Create(fn_temp, shape[1], shape[0], 1, gdal.GDT_Float32)
    TempDataset.SetGeoTransform(gdal_transform)
    if wkt_projection is not None:
        TempDataset.SetProjection(wkt_projection)
    # TODO set csr
    # copy to pcraster format
    outDataset = driver2.CreateCopy(fn, TempDataset, 0)
    # close and cleanup
    TempDataset = None
    outDataset = None
    return fn


def write_map(
    data,
    raster_path,
    nodata,
    transform,
    crs=None,
    clone_path=None,
    pcr_vs="scalar",
    **kwargs,
):
    """Write pcraster map files using pcr.report functionality.

    A PCRaster clone map is written to a temporary directory if not provided.
    For PCRaster types see https://www.gdal.org/frmt_various.html#PCRaster

    Parameters
    ----------
    data : ndarray
        Raster data
    raster_path : str
        Path to output map
    nodata : int, float
        no data value
    transform : affine transform
        Two dimensional affine transform for 2D linear mapping
    clone_path : str, optional
        Path to PCRaster clone map, by default None
    pcr_vs : str, optional
        pcraster type, by default "scalar"

    Raises
    ------
    ImportError
        pcraster package is required
    ValueError
        if invalid ldd
    """
    try:
        import pcraster as pcr
    except ImportError:
        raise ImportError("The pcraster package is required to write map files")
    with tempfile.TemporaryDirectory() as tmpdir:
        # deal with pcr clone map
        if clone_path is None:
            clone_path = write_clone(
                tmpdir,
                gdal_transform=transform.to_gdal(),
                wkt_projection=None if crs is None else CRS.from_user_input(crs).wkt,
                shape=data.shape,
            )
        elif not isfile(clone_path):
            raise IOError(f'clone_path: "{clone_path}" does not exist')
        pcr.setclone(clone_path)
        if nodata is None and pcr_vs != "ldd":
            raise ValueError("nodata value required to write PCR map")
        # write to pcrmap
        if pcr_vs == "ldd":
            # if d8 convert to ldd
            data = data.astype(np.uint8)  # force dtype
            if core_d8.isvalid(data):
                data = core_conversion.d8_to_ldd(data)
            elif not core_ldd.isvalid(data):
                raise ValueError("LDD data not understood")
            mv = int(core_ldd._mv)
            ldd = pcr.numpy2pcr(pcr.Ldd, data.astype(int), mv)
            # make sure it is pcr sound
            # NOTE this should not be necessary
            pcrmap = pcr.lddrepair(ldd)
        elif pcr_vs == "bool":
            pcrmap = pcr.numpy2pcr(pcr.Boolean, data.astype(np.bool), np.bool(nodata))
        elif pcr_vs == "scalar":
            pcrmap = pcr.numpy2pcr(pcr.Scalar, data.astype(float), float(nodata))
        elif pcr_vs == "ordinal":
            pcrmap = pcr.numpy2pcr(pcr.Ordinal, data.astype(int), int(nodata))
        elif pcr_vs == "nominal":
            pcrmap = pcr.numpy2pcr(pcr.Nominal, data.astype(int), int(nodata))
        pcr.report(pcrmap, raster_path)
        # set crs (pcrmap ignores this info from clone ??)
        if crs is not None:
            with rasterio.open(raster_path, "r+") as dst:
                dst.crs = crs
