
import numpy as np
import netCDF4
import section_math
import pandas

class Section(object):
    """
    Class for representing a section spanning from a start to end lat,lon coordinates
    with lat,lon coordinates evenly spaced (in meters) inbetween. Has support for writing a CDO
    gridfile based on the objects attributes.

    Example usage:
    > s = Section("bso", 77., 20., 70., 20.)
    > s.write_gridfile("tmp.grd")
    """

    def __init__(self, name, lat0, lon0, lat1, lon1, interval=10000.0):
        """Constructor setting edge points and interval for section."""
        self.name = name
        self.lat0 = lat0
        self.lon0 = lon0
        self.lat1 = lat1
        self.lon1 = lon1
        self.interval = interval
        self.coors = self.compute_section()

    def compute_section(self):
        """Function that computes lat,lon coordinates between edge
        points with even spacing given by <interval>."""
        azimuth = section_math.calculate_bearing(self.lat0, self.lon0, self.lat1, self.lon1)
        coors = section_math.get_coordinates(self.interval, azimuth, self.lat0, self.lon0, self.lat1, self.lon1)
        return coors

    def write_gridfile(self, filename):
        """Function that writes a gridfile for cdo specfying a section,
        i.e. giving lat,lon coordinates along the section."""
        lats = " ".join([str(l[0]) for l in self.coors])
        lons = " ".join([str(l[1]) for l in self.coors])

        with open(filename, "w") as f:
            f.write("# CDO gridfile for section: {}\n\n".format(self.name))
            f.write("gridtype = curvilinear\n")
            f.write("gridsize = {}\n".format(len(lats)))
            f.write("xsize = {}\n".format(len(lats)))
            f.write("ysize = 1\n")
            f.write("\n")
            f.write("# Longitudes\nxvals = ")
            f.write(lons)
            f.write("\n\n")
            f.write("# Latitudes\nyvals = ")
            f.write(lats)
            f.write("\n")

if __name__ == "__main__":
    # example usage
    s = Section("bso", 77., 20., 70., 20.)
    s.write_gridfile("tmp.grd")
