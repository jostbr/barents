
import subprocess
import netCDF4
import numpy as np
import section
import math_tools

class SectionGrid(section.Section):
    """docstring for SectionGrid."""

    def __init__(self, name, lat0, lon0, lat1, lon1, dx):
        super(SectionGrid, self).__init__(name, lat0, lon0, lat1, lon1, dx)

    def ncks_variable_extract(self, var_list, from_file, to_file):
        """
        Method that writes a new file with a subset of variables from an existing
        file using 'ncks' to extract the desired variables.

        Args:
            var_list (list) : List of variable names to extract with ncks
            from_file (str) : Filename of existing netcdf file
            to_file (str)   : Filename of netcdf file to write to
        """
        var_names = ",".join(v for v in var_list)
        subprocess.call("ncks -O -v {} {} {}".format(var_names, from_file, to_file), shell=True)

    def write_xymesh(self, filename, x_name, y_name, xx_name, yy_name):
        """
        Method that computes a mesgrid from existing 1D projection coordinate variables
        on a netcdf file. Then writes the mesh variables to the same file.

        Args:
            x_name (str)   : Name of existing 1D x-coordinate proj. variable
            y_name (str)   : Name of existing 1D y-coordinate proj. variable
            xx_name (str)  : Name of new 2D x-coordinate proj. mesh variable
            yy_name (str)  : Name of new 2D y-coordinate proj. mesh variable
            filename (str) : Name of netcdf file
        """
        ds = netCDF4.Dataset(filename, mode="r+")
        x = ds.variables[x_name][:]
        y = ds.variables[y_name][:]

        xx, yy = math_tools.meshgrid(x, y)

        x_mesh = ds.createVariable(xx_name, "f8", (y_name, x_name))
        x_mesh.units = "meter"
        x_mesh.standard_name = "x_meshgrid"
        x_mesh.grid_mapping = "stereographic"
        x_mesh.coordinates = "longitude latitude"
        x_mesh[:] = xx

        y_mesh = ds.createVariable(yy_name, "f8", (y_name, x_name))
        y_mesh.units = "meter"
        y_mesh.standard_name = "y_meshgrid"
        y_mesh.grid_mapping = "stereographic"
        y_mesh.coordinates = "longitude latitude"
        y_mesh[:] = yy

        ds.sync()
        ds.close()

    def copy_variable(self, var_name, from_file, to_file):
        """
        Method that copies a variable from one netcdf file and appends it
        to another file using ncks.

        Args:
            from_file (str) : Filename of file containing variable
            to_file (str)   : Filename of file to append variable to
            var_name (str)  : Name of variable to copy
        """
        subprocess.call("ncks -A -v {} {} {}".format(var_name, from_file, to_file), shell=True)

    def write_angle(self, filename, xx_name, yy_name, angle_name):
        """
        Method that computes the angle between model grid and section based on existing
        interpolated projection x- and y meshgrid variables. Then writes the angle to file.

        Args:
            filename (str)   : Filename of netcdf file
            xx_name (str)    : Name of 2D x-coordinate projection variable
            yy_name (str)    : Name of 2D y-coordinate projection variable
            angle_name (str) : Name of angle variable to be written to file
        """
        ds = netCDF4.Dataset(filename, mode="r+")
        xx = ds.variables[xx_name][:]
        yy = ds.variables[yy_name][:]

        angle = math_tools.angle_from_dydx(xx, yy, unit="degrees")

        var = ds.createVariable(angle_name, "f8", ("x"))
        var.units = "degrees"
        var.standard_name = "section_angle"
        var.long_name = "angle_between_section_and_model_grid"
        var.grid_mapping = "stereographic"
        var.coordinates = "longitude latitude"
        var[:] = angle

        ds.sync()
        ds.close()

    def write_area(self, filename, depth_name, model_depth_name, area_name):
        """
        Method that writes the area of each cell in the section to the specified file

        Args:
            skmkdfm
        """
        # read depth levels and model depth from section grid file
        ds = netCDF4.Dataset(filename, mode="r+")
        depth = ds.variables[depth_name][:].copy()
        model_depth = ds.variables[model_depth_name][:].copy()
        area = math_tools.compute_dz(depth, model_depth)*self.dx

        var = ds.createVariable(area_name, "f8", ("depth", "x"))
        var.units = "square meter"
        var.standard_name = "cell_area"
        var.long_name = "area_of_each_cell_in_section"
        var.grid_mapping = "stereographic"
        var.coordinates = "longitude latitude"
        var[:] = area

        ds.sync()
        ds.close()
