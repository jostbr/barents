
import section_grid
import math_tools
import constants

class SectionTransport(SectionGrid):
    """docstring for SectionTransport."""

    def __init__(self, name, lat0, lon0, lat1, lon1, dx):
        super(SectionTransport, self).__init__(name, lat0, lon0, lat1, lon1, dx)

    def write_section_referenced_velocities(self, section_model_file, section_grid_file):
        """
        Rotate u,v velocities in a section data file from model grid to section grid
        and append rotated velocities to section data file. new u velocities are along
        section and new v velocities are across section.

        Args:
            section_grid_file (str)  : Filename of section-interpoalted grid file
            section_model_file (str) : Filename of section-interpoalted model data file
        """
        sdf = Dataset(section_model_file, 'r+')
        u = sdf.variables['u']
        v = sdf.variables['v']

        smg = Dataset(section_grid_file, 'r')
        # alpha is the angel from section x direction to model x direction,
        # section x is defined as along-section and section y is perpendicular to the section
        alpha = smg.variables['alpha']

        u_sec, v_sec = math_tools.rotate_vectorfield(u[:], v[:], -alpha[:]) # rotate from model x to section x

        u_sec_nc = sdf.createVariable('u_sec', u.datatype, u.dimensions)
        u_sec_nc.setncatts({k: u.getncattr(k) for k in u.ncattrs()})
        u_sec_nc.setncatts({'long_name' : 'along_section_velocity'})
        u_sec_nc.setncatts({'standard_name' : 'along_section_velocity'})

        v_sec_nc = sdf.createVariable('v_sec', v.datatype, v.dimensions)
        v_sec_nc.setncatts({k: v.getncattr(k) for k in v.ncattrs()})
        v_sec_nc.setncatts({'long_name' : 'cross_section_velocity'})
        v_sec_nc.setncatts({'standard_name' : 'cross_section_velocity'})

        sdf.close()
        smg.close()

    def compute_transport(self, section_grid_file, section_model_file):
        """
        Method that computes transport through a section assuming section
        referenced velocities are available on file.

        Args:
            section_grid_file (str)  : Filename of section-interpoalted grid file
            section_model_file (str) : Filename of section-interpoalted model data file
        """
        section_grid = Dataset(section_grid_file,'r')
        data_file = Dataset(section_model_file,'r')

        time_nc = data_file.variables['time']
        time = num2date(time_nc[:], time_nc.units)
        cell_area = section_grid.variables['cell_area']
        v = data_file_variables['v_sec']
        temp = data_file.variables['temperature']

        heat_flux = cell_area * np.sum(v, axis=(1,2)) * np.sum(temp, axis(1,2)) * constants.water_density * constants.specific_heat_capacity

        # Calculate running 5-year mean
        dt = time[1]-time[0]
        N = 5*365*24*3600 / dt.total_seconds()
        kernel = sp.ones(N)/N
        heat_flux_5y = sp.convolve(heat_flux, kernel, mode='constant')
