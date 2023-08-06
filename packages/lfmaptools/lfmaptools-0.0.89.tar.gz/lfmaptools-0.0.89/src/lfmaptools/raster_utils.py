import geopandas as gpd
import numpy as np
import pandas as pd
import rioxarray as rxr
import xarray as xr
from scipy.interpolate import griddata, interp1d
from shapely.geometry import (
    LinearRing,
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
    box,
    mapping,
    shape,
)
from skimage.measure import find_contours

# from lfmaptools.epsg_defs import webmerc, wgs84


def raster_flatten(raster):
    rflat = raster.data.flatten()
    return rflat[~np.isnan(rflat)]


def raster_contour(raster, var, cntrs):

    data = raster[var].values
    crs = raster.rio.crs
    x = raster.x
    y = raster.y

    fx = interp1d(np.arange(0, len(x)), x)
    fy = interp1d(np.arange(0, len(y)), y)

    for kk, this_cntr in enumerate(cntrs):

        new_set = True

        cdata = np.zeros_like(data)
        cdata[data >= this_cntr] = 1
        C = find_contours(cdata, 0.5)

        if len(C) == 0:
            pass
        for jj, p in enumerate(C):
            if len(p) > 2:
                p[:, 0] = fy(p[:, 0])
                p[:, 1] = fx(p[:, 1])

                p[:, [0, 1]] = p[:, [1, 0]]

                thisPoly = Polygon(p).buffer(0)

                if not thisPoly.is_empty:
                    if new_set:
                        new_set = False
                        geom = thisPoly

                    else:
                        geom1 = thisPoly

                        geom = geom.symmetric_difference(geom1)

        g_tmp = gpd.GeoDataFrame(columns=["contour", "name", "geometry"], crs=crs)
        g_tmp.loc[0, "contour"] = this_cntr
        g_tmp.loc[[0], "geometry"] = gpd.GeoSeries(geom)
        g_tmp.loc[0, "name"] = var

        if kk == 0:
            g = gpd.GeoDataFrame(g_tmp).set_geometry("geometry")
        else:
            g = gpd.GeoDataFrame(pd.concat([g, g_tmp], ignore_index=True))

    g["contour"] = g["contour"].astype("float64")
    g = g.set_crs(crs)

    return g
