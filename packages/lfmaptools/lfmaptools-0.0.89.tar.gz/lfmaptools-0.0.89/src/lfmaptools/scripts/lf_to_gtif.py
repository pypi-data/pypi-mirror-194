import ast
import os
import pathlib
import sys
import tempfile
import zipfile

import click
import rioxarray as rxr
import xarray as xr

from lfmaptools.netcdf_utils import lfnc
from lfmaptools.textfile_utils import lftxt
from lfmaptools.utilities import _path_of_file_in_zip


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
@click.argument(
    "input_file",
    type=PathPath(
        exists=False,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
    ),
)
@click.option(
    "-d",
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
    help="Destination directory",
)
@click.option(
    "-o",
    "--out_filename",
    "file_out",
    type=click.File(mode="w"),
    is_flag=False,
    flag_value=None,
    help="Output filename",
)
@click.option(
    "-v",
    "--var",
    "var",
    type=click.STRING,
    multiple=True,
    help="Variables to include in output file.  Multiple variables are allowed.",
)
@click.option(
    "--debug",
    "debug",
    is_flag=True,
    help="Run in debug mode with traceback on error messages.",
)
def lf_to_gtif(src, input_file, dest, file_out, var, debug):
    """Convert outputs from LaharFlow into geotiff files.

    SRC is the name of the directory containing LaharFlow outputs, which can be a zipped folder.

    INPUT_FILE is the name of a LaharFlow output file contained in SRC that will be converted to geotif.

    \b
    Example 1:
        For the Maximums.nc file contained in a directory /home/in/
        a geotif containing the maximum_depth and time_of_max_depth variables
        called max_depth.tif can be created in the directoty /home/out/
        using the command:

    \b
        lf_to_gtif -d /home/out/ -o max_depth.tif -v maximum_depth -v time_of_max_depth /home/in/ Maximums.nc

    \b
    Example 2:
        For the 000001.nc file contained in a zipped folder /home/in/LF.zip
        a geotif containing the flow_depth and flow_speed variables
        called 000001.tif can be created in the directoty /home/out/
        using the command:

    \b
        lf_to_gtif -d /home/out/ -o 000001.tif -v flow_depth -v flow_speed /home/in/LF.zip 000001.nc

    """

    sys.tracebacklimit = 1 if debug else 0

    if file_out is None:
        file_out = input_file.with_suffix(".tif")

    if src.is_dir():
        zipped = False
    else:
        if src.suffix == ".zip":
            zipped = True
        else:
            raise ValueError(
                f"Input directory {src} neither a LaharFlow zip file nor a directory"
            )

    if len(var) == 0:
        var = None
    else:
        if type(var) is tuple:
            var = list(var)

    if zipped:
        tmpdirname = tempfile.TemporaryDirectory()
        zipref = zipfile.ZipFile(src, "r")
        infoFilePath = _path_of_file_in_zip("RunInfo.txt", zipref)[0]
        zipref.extract(infoFilePath, tmpdirname.name)
        resultFilePath = _path_of_file_in_zip(input_file.name, zipref)[0]
        zipref.extract(resultFilePath, tmpdirname.name)
        zipref.close()
        dir = tmpdirname.name
    else:
        dir = src
        resultFilePath = input_file

    result_file = os.path.join(dir, resultFilePath)
    result_file_ext = pathlib.Path(result_file).suffix

    if result_file_ext == ".nc":
        data = lfnc(result_file)
    elif result_file_ext == ".txt":
        info_file = os.path.join(dir, "RunInfo.txt")
        data = lftxt(result_file, info_file)
    else:
        raise RuntimeError("result file not recognized")

    if var is not None:
        for v in var:
            if v not in data.vars:
                raise ValueError(
                    f"variable {v} not in {result_file}.\n Allowed variables are {data.vars}"
                )

    raster = data.to_xarray(vars=var)

    fileOut = os.path.join(dest.resolve(), file_out.name)

    print("Writing file to {}".format(fileOut))
    raster.rio.to_raster(fileOut)

    if zipped:
        tmpdirname.cleanup()
