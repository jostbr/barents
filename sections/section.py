
# Functions for reading writing lat,lon sections from file specifying egde
# coordinates to file specifying the entire lat,lon coordinates a long a line
# between the edge points to be used by cdo

import numpy as np
import netCDF4
import section
import pandas

def read_section(filename):
    """Function that reads section edge coordinatesfrom file."""
    return pandas.read_csv(filename, index_col="coordinates")

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

if __name__ == "__main__":
    filename = "cdo_gridfile.txt"
    interval = 10000.0
    lat0 = 77
    lon0 = 20
    lat1 = 70
    lon1 = 20
    azimuth = section.calculate_bearing(lat0,lon0,lat1,lon1)
    coors = section.get_coordinates(interval,azimuth,lat0,lon0,lat1,lon1)
    write_gridfile(filename, coors)
