import ast
import os
import pathlib
import tempfile
import zipfile

import click
import rioxarray as rxr
import utm
import xarray as xr

from lfmaptools.netcdf_utils import lfnc
from lfmaptools.raster_utils import raster_contour
from lfmaptools.utilities import _path_of_file_in_zip, latlon_to_utm_epsg


class PythonLiteralOption(click.Option):
    def type_cast_value(self, ctx, value):
        try:
            return ast.literal_eval(value)
        except:
            raise click.BadParameter(value)


class PathPath(click.Path):
    """A Click path argument that returns a pathlib Path, not a string"""

    def convert(self, value, param, ctx):
        return pathlib.Path(super().convert(value, param, ctx))


@click.command()
@click.argument(
    "src",
    type=PathPath(
        exists=True,
        file_okay=True,
        dir_okay=True,
        writable=False,
        readable=True,
    ),
)
@click.option(
    "-dest",
    "--dest",
    "dest",
    type=PathPath(
        exists=False,
        file_okay=False,
        dir_okay=True,
        writable=True,
        readable=True,
    ),
    prompt="Set destination directory",
    default=os.getcwd(),
)
@click.option(
    "-o",
    "--out_filename",
    "file_out",
    type=click.File(mode="w"),
    is_flag=False,
    flag_value=None,
)
@click.option(
    "-t",
    "--threshold",
    "threshold",
    type=click.FLOAT,
    multiple=True,
)
def lf_inundation(src, dest, file_out, threshold):

    if src.is_dir():
        zipped = False
    else:
        if src.suffix == ".zip":
            zipped = True
        else:
            raise ValueError(
                f"Input directory {src} neither a LaharFlow zip file nor a directory"
            )

    with tempfile.TemporaryDirectory() as tmpdirname:

        if zipped:
            zipref = zipfile.ZipFile(src, "r")
            infoFilePath = _path_of_file_in_zip("RunInfo.txt", zipref)[0]
            zipref.extract(infoFilePath, tmpdirname)

            resultFilePath = _path_of_file_in_zip("Maximums.nc", zipref)[0]
            zipref.extract(resultFilePath, tmpdirname)

            zipref.close()

            info_file = os.path.join(tmpdirname, "RunInfo.txt")
            result_file = os.path.join(tmpdirname, resultFilePath)

            ncdata = lfnc(result_file)

            centre_latitude = ncdata.get_attr("centre_latitude")
            centre_longitude = ncdata.get_attr("centre_longitude")

            utm_full = utm.from_latlon(centre_latitude, centre_longitude)
            utmCode = latlon_to_utm_epsg(centre_latitude, centre_longitude)

            raster = ncdata.to_xarray(vars=["maximum_depth"])

            coords = list(raster.coords.keys())
            if "x_distance" in coords:
                raster = raster.rename({"x_distance": "x"})
            if "y_distance" in coords:
                raster = raster.rename({"y_distance": "y"})
            raster["x"] = raster["x"] + utm_full[0]
            raster["y"] = raster["y"] + utm_full[1]
            raster.rio.write_crs(utmCode, inplace=True)

            g = raster_contour(raster, "maximum_depth", list(threshold))

            g.to_file("inundation.shp")

        else:
            print("Currently only works for netcdf files")
            return
            # info_file = os.path.join(input_dir, "RunInfo.txt")
            # if not os.path.isfile(info_file):
            #     print(f"Run info file {info_file} does not exist")
            # result_file = os.path.join(input_dir, input_file.name)

    fileOut = os.path.join(dest.resolve(), file_out.name)

    print("Writing file to {}".format(fileOut))
    g.to_file(fileOut)
