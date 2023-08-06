import ast
import os
import pathlib
import sys
import tempfile
import zipfile

import click
import rioxarray as rxr
import xarray as xr

from lfmaptools.kml_utils import raster2kml
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
    multiple=False,
    required=True,
    help="Variable to include in kml file.  Only single variable is allowed.",
)
@click.option(
    "--vmin",
    "vmin",
    type=click.FLOAT,
    multiple=False,
    help="Lower threshold of data values.  Values below vmin are not included in the kml file.",
)
@click.option(
    "--vmax",
    "vmax",
    type=click.FLOAT,
    multiple=False,
    help="Upper threshold of data values.  Values above vmax have the same colour as values equal to vmax.",
)
@click.option(
    "--vcenter",
    "vcenter",
    type=click.FLOAT,
    multiple=False,
    default=0.0,
    help="Value used for the central value for diverging colour maps. Default vcentre=0",
)
@click.option(
    "--vcut",
    "vcut",
    type=click.Tuple([float, float]),
    nargs=2,
    multiple=False,
    default=(None, None),
    help="Threshold values used around the central value vcenter for diverging colour maps. Values between the vcut values are neglected.",
)
@click.option(
    "--cmap",
    "cmap",
    type=click.STRING,
    multiple=False,
    default="viridis",
    help="Colour map used to colour kml cells.  Must be a Matplotlib colormap, see <https://matplotlib.org/stable/tutorials/colors/colormaps.html>.  Default cmap=viridis",
)
@click.option(
    "-n",
    "--normalization",
    "normalization",
    type=click.Choice(["Linear", "Log", "TwoSlopeNorm"]),
    multiple=False,
    default="Linear",
    help="Normalization method for the data range.  See <https://matplotlib.org/stable/tutorials/colors/colormapnorms.html>.  Default cmap=Linear",
)
@click.option(
    "-e",
    "--extrude",
    "extrude",
    is_flag=True,
    help="Extrude kml polygons to be three-dimensional.",
)
@click.option(
    "-a",
    "--alpha",
    "alpha",
    type=click.FloatRange(0, 1),
    multiple=False,
    default=1.0,
    help="Set alpha channel opacity, in range 0<=alpha<=1.  alpha=0 for fully transparent; alpha=1 for fully opaque. Default alpha=1",
)
@click.option(
    "--debug",
    "debug",
    is_flag=True,
    help="Run in debug mode with traceback on error messages.",
)
def lf_to_kml(
    src,
    input_file,
    dest,
    file_out,
    var,
    vmin,
    vmax,
    vcenter,
    vcut,
    cmap,
    normalization,
    extrude,
    alpha,
    debug,
):

    """Convert outputs from LaharFlow into kml files.

    SRC is the name of the directory containing LaharFlow outputs, which can be a zipped folder.

    INPUT_FILE is the name of a LaharFlow output file contained in SRC that will be converted to geotif.

    \b
    Example 1:
        For the Maximums.nc file contained in a directory /home/in/
        a kml file containing the maximum_depth variable
        called max_depth.kml can be created in the directoty /home/out/
        using the command:

    \b
        lf_to_kml -d /home/out/ -o max_depth.kml -v maximum_depth /home/in/ Maximums.nc

    \b
    Example 2:
        For the 000001.nc file contained in a zipped folder /home/in/LF.zip
        a kml file containing the flow_depth variable
        called 000001.kml can be created in the directoty /home/out/
        using the command:

    \b
        lf_to_kml -d /home/out/ -o 000001.kml -v flow_depth /home/in/LF.zip 000001.nc

    \b
    Example 3:
        For the 000010.txt file contained in a directory /home/in/
        a kml file containing the elevation_change variable
        called elev_change_10.kml can be created in the directoty /home/out/
        using the command:

    \b
        lf_to_kml -d /home/out/ -o elev_change_10.kml -v elevation_change -a 1 --cmap=coolwarm --normalization=TwoSlopeNorm --vcenter=0 --vcut=-0.01 0.01 /home/in/ 000010.txt
    """

    sys.tracebacklimit = 1 if debug else 0

    if file_out is None:
        file_out = input_file.with_suffix(".kml")

    if src.is_dir():
        zipped = False
    else:
        if src.suffix == ".zip":
            zipped = True
        else:
            raise ValueError(
                f"Input directory {src} neither a LaharFlow zip file nor a directory"
            )

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

    if var not in data.vars:
        raise ValueError(
            f"variable {var} not in {result_file}.\n Allowed variables are {data.vars}"
        )

    raster = data.to_xarray(vars=var)

    fileOut = os.path.join(dest.resolve(), file_out.name)
    print("Writing file to {}".format(fileOut))

    vcut = list(vcut)

    raster2kml(
        raster,
        var,
        fileOut,
        resampling="cubic",
        vmin=vmin,
        vmax=vmax,
        vcenter=vcenter,
        vcut=vcut,
        cmap=cmap,
        normalization=normalization,
        extrude=extrude,
        alpha=alpha,
    )

    if zipped:
        tmpdirname.cleanup()
