
import os
import netCDF4
import math_tools

class GridFile(object):
    """docstring for SectionGrid."""

    def __init__(self, grid_file):
        """
        Constructor opening grid file in mode r+.

        Args:
            grid_file (str) : File of existing grid file
        """
        if not os.path.exists(grid_file):
            raise IOError("This class assumes file {} exists!".format(grid_file))

        self.grid_file = grid_file

    def write_angle(self, angle_name):
        """
        Function that commpute and write angle between north direction relative
        to grid positive y coordinate.

        Args:
            angle_name (str) : Name of angle variable to be written to grid file
        """
        with netCDF4.Dataset(self.grid_file, mode="r+") as grid:
            try:
                latitude = grid.variables["latitude"]
            except KeyError:
                raise ValueError("Grid file {} must contain latitude variable!".format(self.grid_file))

            angle = math_tools.compute_angle_relative_to_north(latitude[:,:])

            var = grid.createVariable(angle_name, "f8", ("y", "x"))
            var.units = "degrees"
            var.standard_name = "angle"
            var.long_name = "angle_between_north_and_model_ydir"
            var.grid_mapping = "stereographic"
            var.coordinates = "longitude latitude"
            var[:] = angle
            grid.sync()

    def write_xymesh(self, x_name, y_name, xx_name, yy_name):
        """
        Method that computes a mesgrid from existing 1D projection coordinate variables
        on netcdf grid file. Then writes the mesh variables to the grid file.

        Args:
            x_name (str)   : Name of existing 1D x-coordinate proj. variable
            y_name (str)   : Name of existing 1D y-coordinate proj. variable
            xx_name (str)  : Name of new 2D x-coordinate proj. mesh variable
            yy_name (str)  : Name of new 2D y-coordinate proj. mesh variable
        """
        with netCDF4.Dataset(self.grid_file, mode="r+") as grid:
            x = grid.variables[x_name][:]
            y = grid.variables[y_name][:]

            xx, yy = math_tools.meshgrid(x, y)

            x_mesh = grid.createVariable(xx_name, "f8", (y_name, x_name))
            x_mesh.units = "meter"
            x_mesh.standard_name = "x_meshgrid"
            x_mesh.grid_mapping = "stereographic"
            x_mesh.coordinates = "longitude latitude"
            x_mesh[:] = xx

            y_mesh = grid.createVariable(yy_name, "f8", (y_name, x_name))
            y_mesh.units = "meter"
            y_mesh.standard_name = "y_meshgrid"
            y_mesh.grid_mapping = "stereographic"
            y_mesh.coordinates = "longitude latitude"
            y_mesh[:] = yy

            grid.sync()
