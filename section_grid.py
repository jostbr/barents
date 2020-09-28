
import os
import subprocess
import netCDF4
import numpy as np
import section
import math_tools

class SectionGridFile(object):
    """docstring for SectionGridFile."""

    def __init__(self, section, section_grid_file):
        """
        Constructor setting attributes and calling superclass constructor.

        Args:
            section (Section)     : Section object to make grid file for
            grid_model_file (str) : Name of file to contain inteprolated grid data along section,
                                       will be filled when calling self.interpolate()
        """
        self.section = section
        self.section_grid_file = section_grid_file

    def interpolate(self, grid_file):
        """
        Method that calls Section interpolate method.

        Args:
            grid_file (str) : Grid file to be interpoalted onto section.
        """
        if os.path.exists(self.section_grid_file):
            print("WARNING: Overwriting section grid file {}".format(self.section_grid_file))

        self.section.interpolate(grid_file, self.section_grid_file)

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
        raise NotImplementedError("old code, might be removed in the future")
        if not os.path.exists(self.section_grid_file):
            raise RuntimeError("Section grid file {} must exists before calling this method!".format(self.section_grid_file))

        with netCDF4.Dataset(self.section_grid_file, mode="r+") as section_grid:
            xx = section_grid.variables[xx_name][:]
            yy = section_grid.variables[yy_name][:]

            angle = math_tools.angle_from_dydx(xx, yy, unit="degrees")

            var = section_grid.createVariable(angle_name, "f8", ("x"))
            var.units = "degrees"
            var.standard_name = "section_angle"
            var.long_name = "angle_between_section_and_model_grid"
            var.grid_mapping = "stereographic"
            var.coordinates = "longitude latitude"
            var[:] = angle

            section_grid.sync()

    def write_area(self, depth_name, model_depth_name, area_name):
        """
        Method that based on the depth layers and model depth in the section,
        computes and writes the area of each cell in the section to the specified file

        Args:
            depth_name (str) : Name of depth variable
            model_depth_name (str) : Name of model depth (topography) variable
            area_name (str) : Name of cell area variable to be written
        """
        if not os.path.exists(self.section_grid_file):
            raise RuntimeError("Section grid file {} must exists before calling this method!".format(self.section_grid_file))

        with netCDF4.Dataset(self.section_grid_file, mode="r+") as section_grid:
            depth = section_grid.variables[depth_name][:].copy()
            model_depth = section_grid.variables[model_depth_name][:].copy()
            area = math_tools.compute_dz(depth, model_depth)*self.section.dx

            var = section_grid.createVariable(area_name, "f8", ("depth", "x"))
            var.units = "square meter"
            var.standard_name = "cell_area"
            var.long_name = "area_of_each_cell_in_section"
            var.grid_mapping = "stereographic"
            var.coordinates = "longitude latitude"
            var[:] = area

            section_grid.sync()
