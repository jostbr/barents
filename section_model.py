
import os
import netCDF4
import numpy as np
import section_grid
import math_tools
import constants

class SectionModelFile(object):
    """docstring for SectionModelFile."""

    def __init__(self, section, section_model_file):
        """
        Constructor setting attributes.

        Args:
            section (Section)        : Section objects defining the section of interest
            section_model_file (str) : Name of file to contain inteprolated model data along section,
                                       will be filled when calling self.interpolate()
        """
        self.section = section
        self.section_model_file = section_model_file
        self.section_grid_file = None  # will be set in either self.set_section_grid or self.generate_section_grid

    def set_section_grid(self, section_grid_file):
        """
        Method to use if section grid file already exists.

        Args:
            section_grid_file (str) : Name of existing section grid file
        """
        self.section_grid_file = section_grid_file

    def generate_section_grid(self, grid_file, section_grid_file):
        """
        Method to use if making section grid file in the process. After calling this the
        self.section_grid attribute will be set to the opened section grid file in the superclass.

        Args:
            grid_file (str)         : Name of grid file to be interpolated to section
            section_grid_file (str) : Name of section grid file to be created
        """
        sg = section_grid.SectionGridFile(section, section_grid_file)
        sg.interpolate(grid_file)
        self.set_section_grid(sg.section_grid_file)

    def interpolate(self, model_file):
        """
        Method that calls Section interpolate method.

        Args:
            model_file (str) : Model data file to be interpolated onto section
        """
        self.section.interpolate(model_file, self.section_model_file)

    def write_section_referenced_velocities(self):
        """
        Rotate u,v velocities in a section data file from model grid to section grid
        and append rotated velocities to section data file. New u velocities are along
        section and new v velocities are across section.

        Args:
            section_grid_file (str)  : Filename of section-interpoalted grid file
            section_model_file (str) : Filename of section-interpoalted model data file
        """
        if self.section_grid_file is None:
            raise RuntimeError("self.set_section_grid or self.generate_section_grid must be called before modifying section model file!")
        if not os.path.exists(self.section_model_file):
            raise RuntimeError("self.interpolate must be called before modifying section model file!")

        # read angle from section grid file
        with netCDF4.Dataset(self.section_grid_file, "r") as section_grid:
            # alpha is the angel from section x direction to model x direction,
            # section x is defined as along-section and section y is perpendicular to the section
            alpha = section_grid.variables["angle"]
            alpha = np.column_stack([alpha for _ in range(12)]).T

        # read u,v from section model file and compute+write u_sec,v_sec
        with netCDF4.Dataset(self.section_model_file, "r+") as section_model:
            u = section_model.variables["u"]
            v = section_model.variables["v"]
            print(u.shape, v.shape, alpha.shape)
            u_sec, v_sec = math_tools.rotate_vectorfield(u[0,:,:], v[0,:,:], -alpha[:]) # rotate from model x to section x

            u_sec_nc = section_model.createVariable("u_sec", u.datatype, u.dimensions)
            u_sec_nc.setncatts({k: u.getncattr(k) for k in u.ncattrs()})
            u_sec_nc.setncatts({"long_name" : "along_section_velocity"})
            u_sec_nc.setncatts({"standard_name" : "along_section_velocity"})
            section_model.variables["u_sec"][0,:,:] = u_sec

            v_sec_nc = section_model.createVariable("v_sec", v.datatype, v.dimensions)
            v_sec_nc.setncatts({k: v.getncattr(k) for k in v.ncattrs()})
            v_sec_nc.setncatts({"long_name" : "cross_section_velocity"})
            v_sec_nc.setncatts({"standard_name" : "cross_section_velocity"})
            section_model.variables["v_sec"][0,:,:] = v_sec

            section_model.sync()

    def compute_transport(self, section_grid_file, section_model_file):
        """
        Method that computes transport through a section assuming section
        referenced velocities are available on file.

        Args:
            section_grid_file (str)  : Filename of section-interpoalted grid file
            section_model_file (str) : Filename of section-interpoalted model data file
        """
        raise NotImplementedError("needs further dev and testing")
        section_grid = Dataset(section_grid_file,"r")
        data_file = Dataset(section_model_file,"r")

        time_nc = data_file.variables["time"]
        time = num2date(time_nc[:], time_nc.units)
        cell_area = section_grid.variables["cell_area"]
        v = data_file_variables["v_sec"]
        temp = data_file.variables["temperature"]

        heat_flux = cell_area * np.sum(v, axis=(1,2)) * np.sum(temp, axis=(1,2)) * constants.water_density * constants.specific_heat_capacity

        # Calculate running 5-year mean
        dt = time[1]-time[0]
        N = 5*365*24*3600 / dt.total_seconds()
        kernel = sp.ones(N)/N
        heat_flux_5y = sp.convolve(heat_flux, kernel, mode="constant")
