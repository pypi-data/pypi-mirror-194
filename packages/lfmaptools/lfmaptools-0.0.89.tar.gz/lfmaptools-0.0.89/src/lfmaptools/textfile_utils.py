import csv

import pandas as pd
import utm
import xarray as xa
from numpy import fromstring

from lfmaptools.lfsourceclass import LFSource
from lfmaptools.utilities import latlon_to_utm_epsg


class lftxt(object):
    def __init__(self, filename, infofile):

        self.filename = filename

        self.infofile = infofile

        self.data = txt2pd(filename)

        self.vars = txt_vars(filename)

        self.centre_latitude = self.get_attr("Latitude of domain centre")
        self.centre_longitude = self.get_attr("Longitude of domain centre")

    def get_attr(self, attr):

        if attr == "Source":
            val = []
        else:
            val = None

        with open(self.infofile) as f:
            for ln, line in enumerate(f):
                if attr in line:

                    if attr == "Input file name":
                        val = (line.split(":", 1)[1]).strip(" \t\n\r")
                        break
                    if attr == "Latitude of domain centre":
                        val = float(line.split("=", 1)[1])
                        break
                    if attr == "Longitude of domain centre":
                        val = float(line.split("=", 1)[1])
                        break
                    if attr == "Time step between outputs":
                        val = float(line.split("=", 1)[1])
                        break
                    if attr == "height threshold":
                        val = float(line.split("=", 1)[1])
                        break
                    if attr == "nTiles":
                        val = int(line.split("=", 1)[1])
                        break
                    if attr == "nXtiles":
                        val = int(line.split("=", 1)[1])
                        break
                    if attr == "nYtiles":
                        val = int(line.split("=", 1)[1])
                        break
                    if attr == "nXpertile":
                        val = int(line.split("=", 1)[1])
                        break
                    if attr == "nYpertile":
                        val = int(line.split("=", 1)[1])
                        break
                    if attr == "Xtilesize":
                        val = float(line.split("=", 1)[1])
                        break
                    if attr == "Ytilesize":
                        val = float(line.split("=", 1)[1])
                        break
                    if attr == "xSize":
                        val = float(line.split("=", 1)[1])
                        break
                    if attr == "ySize":
                        val = float(line.split("=", 1)[1])
                        break
                    if attr == "nXPoints":
                        val = int(line.split("=", 1)[1])
                        break
                    if attr == "nYPoints":
                        val = int(line.split("=", 1)[1])
                        break
                    if attr == "deltaX":
                        val = float(line.split("=", 1)[1])
                        break
                    if attr == "deltaY":
                        val = float(line.split("=", 1)[1])
                        break
                    if attr == "Number of output files":
                        val = int(line.split("=", 1)[1])
                        break
                    if attr == "Last output file":
                        val = int(line.split("=", 1)[1])
                        break
                    if attr == "end time":
                        val = float(line.split("=", 1)[1])
                        break
                    if attr == "Time step between outputs":
                        val = float(line.split("=", 1)[1])
                        break
                    if attr == "rhow":
                        val = float(line.split("=", 1)[1])
                        break
                    if attr == "rhos":
                        val = float(line.split("=", 1)[1])
                        break
                    if attr == "Erosion depth":
                        val = float(line.split("=", 1)[1])
                        break
                    if attr == "Topography type":
                        val = (line.split("=", 1)[1]).strip(" \t\n\r")
                        break
                    if attr == "Topography path":
                        val = line.split("=", 1)[1].strip(" \t\n\r")
                        break
                    if attr == "Raster path":
                        val = line.split("=", 1)[1].strip(" \t\n\r")
                        break
                    if attr == "Raster file":
                        val = line.split("=", 1)[1].strip(" \t\n\r")
                        break
                    if attr == "SRTM path":
                        val = line.split("=", 1)[1].strip(" \t\n\r")
                        break
                    if attr == "SRTM files":
                        fileList = line.split("=", 1)[1]
                        fileList = fileList.strip("\n")
                        fileList = fileList.strip()
                        SRTMFiles = fileList.split(",")
                        val = list(filter(None, SRTMFiles))
                        break
                    if attr == "SRTM virtual file":
                        val = line.split("=", 1)[1].strip(" \t\n\r")
                        break
                    if attr == "Embedded raster":
                        val = line.split("=", 1)[1].strip()
                        break
                    if attr == "Land use path":
                        val = line.split("=", 1)[1].strip(" \t\n\r")
                        break
                    if attr == "Land use file":
                        val = line.split("=", 1)[1].strip(" \t\n\r")
                        break
                    if attr == "Source":
                        s_x = float(next(f).split("=", 1)[1].rstrip())
                        s_y = float(next(f).split("=", 1)[1].rstrip())
                        s_lat = float(next(f).split("=", 1)[1].rstrip())
                        s_lon = float(next(f).split("=", 1)[1].rstrip())
                        s_radius = float(next(f).split("=", 1)[1].rstrip())
                        s_time = fromstring(
                            next(f)
                            .split("=", 1)[1]
                            .rstrip()
                            .replace("(", "")
                            .replace(")", ""),
                            sep=",",
                        )
                        s_flux = fromstring(
                            next(f)
                            .split("=", 1)[1]
                            .rstrip()
                            .replace("(", "")
                            .replace(")", ""),
                            sep=",",
                        )
                        s_conc = fromstring(
                            next(f)
                            .split("=", 1)[1]
                            .rstrip()
                            .replace("(", "")
                            .replace(")", ""),
                            sep=",",
                        )

                        val.append(
                            LFSource(
                                x=s_x,
                                y=s_y,
                                lat=s_lat,
                                lon=s_lon,
                                radius=s_radius,
                                time=s_time,
                                flux=s_flux,
                                conc=s_conc,
                            )
                        )

        return val

    def to_xarray(self, vars=None):

        x_var = "x_distance" if "x_distance" in self.vars else "x"
        y_var = "y_distance" if "y_distance" in self.vars else "y"

        if vars is not None:
            if type(vars) is not list:
                vars = [vars]
            for v in vars:
                if v not in self.vars:
                    raise ValueError(
                        f"variable {v} not in {self.filename}.\n Allowed variables are {self.vars}"
                    )
            drop_vars = [d for d in self.data.columns if d not in vars]
        else:
            drop_vars = [d for d in self.data.columns]

        data = self.data.drop(columns=drop_vars, axis=1, inplace=False)

        raster = xa.Dataset.from_dataframe(data)

        if x_var == "x_distance":
            raster = raster.rename({"x_distance": "x"})
        if y_var == "y_distance":
            raster = raster.rename({"y_distance": "y"})

        if self.centre_latitude is not None and self.centre_longitude is not None:
            utm_full = utm.from_latlon(self.centre_latitude, self.centre_longitude)
            utmCode = latlon_to_utm_epsg(self.centre_latitude, self.centre_longitude)
            raster["x"] = raster["x"] + utm_full[0]
            raster["y"] = raster["y"] + utm_full[1]
            raster.rio.write_crs(utmCode, inplace=True)

        return raster


def txt_vars(filename):

    with open(filename, "r") as f:
        reader = csv.reader(f)
        header = next(reader, None)

    vars = [h.strip() for h in header]

    return vars


def txt2pd(filename, vars=None):

    # print(f"vars = {vars}")
    # print(txt_vars(filename))

    data = pd.read_csv(
        filename,
        delimiter=",",
        skipinitialspace=True,
        index_col=["y_distance", "x_distance"],
    )

    if vars is not None:
        drop_vars = [d for d in data.columns if d not in vars]
        data.drop(columns=drop_vars, axis=1, inplace=True)

    return data


def txt2xr(filename, vars=None):

    data = txt2pd(filename, vars=vars)
    raster = xa.Dataset.from_dataframe(data)

    return raster
