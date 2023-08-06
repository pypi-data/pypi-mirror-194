import os
import pathlib

import matplotlib as mpl
import matplotlib.colors as mpc
import numpy as np
import pandas as pd
import rioxarray as rxa
import xarray as xa
from rasterio.enums import Resampling

from lfmaptools.epsg_defs import wgs84


def raster2kml(
    data,
    var,
    filename,
    resampling="cubic",
    vmin=0.01,
    vmax=None,
    vcenter=0,
    vcut=[None, None],
    cmap="viridis",
    normalization="Linear",
    extrude=True,
    alpha=0,
):

    if resampling not in [r.name for r in Resampling]:
        raise ValueError(
            f"resampling choice {resampling} not recognized. \n Allowed values are {[r.name for r in Resampling]}"
        )

    data_wgs84 = data.rio.reproject(
        wgs84, resampling=Resampling[resampling], nodata=np.nan
    )

    res_x, res_y = data_wgs84.rio.resolution()
    res_y = -res_y

    if vmin is None:
        vmin = float(data_wgs84[var].min().values)
    if vmax is None:
        vmax = float(data_wgs84[var].max().values)

    if normalization == "Linear":
        norm = mpc.Normalize(vmin=vmin, vmax=vmax)
    elif normalization == "Log":
        norm = mpc.LogNorm(vmin=vmin, vmax=vmax)
    elif normalization == "TwoSlopeNorm":
        norm = mpc.TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)
    else:
        raise ValueError(f"normalization {normalization} not recognized")

    cmap = mpl.colormaps[cmap]

    if vcut[0] is None:
        vcut[0] = np.inf
    if vcut[1] is None:
        vcut[1] = -np.inf

    with open(filename, mode="w+") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        f.write("  <Document>\n")
        for j, lat in enumerate(data_wgs84.y.values):
            for i, lon in enumerate(data_wgs84.x.values):
                val = data_wgs84[var][j, i].values
                if val < vmin or (val > vcut[0] and val < vcut[1]):
                    pass
                else:
                    color = cmap(norm(val), alpha=alpha)
                    mpc_cstring = mpc.to_hex(color, keep_alpha=True)
                    mpc_cstring = mpc_cstring.strip("#")
                    cstring = (
                        mpc_cstring[6:8]
                        + mpc_cstring[4:6]
                        + mpc_cstring[2:4]
                        + mpc_cstring[0:2]
                    )
                    f.write("    <Placemark>\n")
                    f.write('      <Style id="examplePolyStyle">\n')
                    f.write("        <PolyStyle>\n")
                    f.write("          <color>\n")
                    f.write(f"            {cstring}\n")
                    f.write("          </color>\n")
                    f.write("          <colorMode>normal</colorMode>\n")
                    f.write("          <outline>0</outline>\n")
                    f.write("        </PolyStyle>\n")
                    f.write("      </Style>\n")
                    f.write("      <Polygon>\n")
                    if extrude:
                        f.write("        <extrude>1</extrude>\n")
                        f.write(
                            "        <altitudeMode>relativeToGround</altitudeMode>\n"
                        )
                    else:
                        f.write("        <extrude>0</extrude>\n")
                        f.write("        <altitudeMode>clampToGround</altitudeMode>\n")
                    f.write("        <outerBoundaryIs>\n")
                    f.write("          <LinearRing>\n")
                    f.write("            <coordinates>\n")
                    for s in [[-1, 1], [1, 1], [1, -1], [-1, -1], [-1, 1]]:
                        f.write(
                            f"              {lon+0.5*s[0]*res_x},{lat+0.5*s[1]*res_y},{val}\n"
                        )
                    f.write("            </coordinates>\n")
                    f.write("          </LinearRing>\n")
                    f.write("        </outerBoundaryIs>\n")
                    f.write("      </Polygon>\n")
                    f.write("    </Placemark>\n")
        f.write("  </Document>\n")
        f.write("</kml>")
