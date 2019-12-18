
# Functions for reading writing lat,lon sections from file specifying egde
# coordinates to file specifying the entire lat,lon coordinates a long a line
# between the edge points to be used by cdo

import math
import numpy as np
import netCDF4
import section

def read_section(filename):
    """Function that reads section edge coordinatesfrom file."""
    raise NotImplementedError

def write_gridfile(filename, coors):
    """Function that writes a gridfile for cdo specfying a section,
    i.e. giving lat,lon coordinates along the section."""
    lats = ",".join([str(l[0]) for l in coors])
    lons = ",".join([str(l[1]) for l in coors])

    with open(filename, "w") as f:
        f.write("gridtype = curvilinear\n")
        f.write("gridsize = {}\n".format(len(lats)))
        f.write("xsize = {}\n".format(len(lats)))
        f.write("ysize = 1\n")
        f.write("\n")
        f.write("# Longitudes\n")
        print(lons)
        f.write(lons)
        f.write("\n\n")
        f.write("# Latitudes\n")
        f.write(lats)
        f.write("\n")
