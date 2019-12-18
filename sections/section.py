
# Functions for reading writing lat,lon sections from file specifying egde
# coordinates to file specifying the entire lat,lon coordinates a long a line
# between the edge points to be used by cdo

import numpy as np
import netCDF4
import compute_section
import pandas

class Section():
    def __init__(self, lat0, lon0, lat1, lon1, interval=10000.0):
        """Constructor setting edge points and interval for section."""
        self.lat0 = lat0
        self.lon0 = lon0
        self.lat1 = lat1
        self.lon1 = lon1
        self.coors = self.compute_section(interval)

    def compute_section(self, interval):
        """Function that computes lat,lon coordinates between edge
        points with even spacing given by <interval>."""
        azimuth = compute_section.calculate_bearing(self.lat0, self.lon0, self.lat1, self.lon1)
        coors = compute_section.get_coordinates(interval, azimuth, self.lat0, self.lon0, self.lat1, self.lon1)
        print(coors)
        return coors

    def write_gridfile(self, filename):
        """Function that writes a gridfile for cdo specfying a section,
        i.e. giving lat,lon coordinates along the section."""
        lats = ",".join([str(l[0]) for l in self.coors])
        lons = ",".join([str(l[1]) for l in self.coors])

        with open(filename, "w") as f:
            f.write("gridtype = curvilinear\n")
            f.write("gridsize = {}\n".format(len(lats)))
            f.write("xsize = {}\n".format(len(lats)))
            f.write("ysize = 1\n")
            f.write("\n")
            f.write("# Longitudes\n")
            f.write(lons)
            f.write("\n\n")
            f.write("# Latitudes\n")
            f.write(lat s)
            f.write("\n")

if __name__ == "__main__":
    s = Section(77,20,70,20)
    s.write_gridfile("tmp.txt")
