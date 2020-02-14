
# Script to append meshgrid of model x and y coordinates to netcdf file

import os
import argparse
import netCDF4
import numpy as np

def valid_path(path):
    """Function that validates if path exists."""
    if os.path.exists(path):
        return path
    else:
        raise argparse.ArgumentTypeError("Invalid path {}!".format(path))

# handle command line arguments
parser = argparse.ArgumentParser(description="Compute and append 2D meshgrid of existing 1D x,y-coordinates")
parser.add_argument("filename", type=valid_path, help="filename of netcdf file")
parser.add_argument("x_name", type=str, help="variable name of 1D x-coordinate")
parser.add_argument("y_name", type=str, help="variable name of 1D y-coordinate")
args = parser.parse_args()

# open dataset and read 1D coordinates
ds = netCDF4.Dataset(args.filename, mode="r+")
x = ds.variables[args.x_name][:]
y = ds.variables[args.y_name][:]

# compute 2D coordinates
xx, yy = np.meshgrid(y, x)

# add x 2D variable
x_mesh = ds.createVariable("x_mesh", "f8", ("x", "y"))
x_mesh.units = "meter"
x_mesh.standard_name = "x_meshgrid"
x_mesh.grid_mapping = "stereographic"
x_mesh.coordinates = "longitude latitude"
x_mesh[:] = xx

# add y 2D variable
y_mesh = ds.createVariable("y_mesh", "f8", ("x", "y"))
y_mesh.units = "meter"
y_mesh.standard_name = "y_meshgrid"
y_mesh.grid_mapping = "stereographic"
y_mesh.coordinates = "longitude latitude"
y_mesh[:] = yy

ds.sync()
ds.close()
