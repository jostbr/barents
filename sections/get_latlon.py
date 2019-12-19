
# Functions for getting latitude and longitude arrays from CDO gridfile and topaz grid file

import netCDF4
import numpy as np

def get_latlon_from_cdo_gridfile(filename):
    """Function that reads latitude and longitude arrays from CDO gridfile
    and returns them as 1D arrays."""
    array_from_line = lambda l: np.array([float(v) for v in line.split()[2:]])

    with open(filename, "r") as f:
        for line in f:
            if "xvals" in line:
                lons = array_from_line(line)
            elif "yvals" in line:
                lats = array_from_line(line)

    return lats, lons

def get_latlon_from_topaz(filename):
    """Function that gets latitude and longitude arrays from TOPAZ
    grid file and returns them as 2D arrays."""
    ds = netCDF4.Dataset(filename, mode="r")
    lats = ds.variables["latitude"][:,:]
    lons = ds.variables["longitude"][:,:]
    return lats, lons

if __name__ == "__main__":
    lat_cdo, lon_cdo = get_latlon_from_cdo_gridfile("data/barents_sea_opening_50km.grd"))
    lat_topaz, lon_topaz = get_latlon_from_topaz("/lustre/storeA/users/johannesro/BS_topaz/topaz_grid.nc"))
