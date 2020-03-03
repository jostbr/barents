
import netCDF4
import numpy as np
import section_transport
import math_tools

# define filenames
topaz_file = "https://thredds.met.no/thredds/dodsC/myocean/arc-mfc/ran-arc-myoceanv2/topaz_V4_myocean_arctic_grid1to8_da_class1_20181215.nc"
topaz_aggr_file = "https://thredds.met.no/thredds/dodsC/topaz/dataset-ran-arc-myoceanv2-be"
topaz_data_file = "test.nc"
cdo_grid_file = "bso.grd"
grid_file = "topaz_grid.nc"
section_grid_file = "topaz_grid_bso.nc"
section_data_file = "topaz_data_bso.nc"

# use SectionTransport object to do all section based stuff
st = section_transport.SectionTransport("bso", 68.0, 20.0, 76.0, 18.0, 5000.0)
st.write_section(cdo_grid_file)                                                                  # create cdo section definition file
st.ncks_variable_extract(["stereographic", "depth", "model_depth"], topaz_data_file, grid_file)  # create full domain gridfile
st.write_xymesh(grid_file, "x", "y", "x_mesh", "y_mesh")                                         # write x,y meshgrid to gridfile
st.interpolate(cdo_grid_file, grid_file, section_grid_file)                                      # interpolate gridfile to section
st.write_angle(section_grid_file, "x_mesh", "y_mesh", "angle")                                   # compute and write angle to section gridfile
st.ncks_copy_variable("depth", grid_file, section_grid_file)                                     # copy depth from full gridfile to section gridfile
st.write_area(section_grid_file, "depth", "model_depth", "cell_area")                            # compute and write area of cells to gridfile
#st.interpolate(cdo_grid_file, topaz_data_file, section_data_file)                               # interpolate model data file to section
st.write_section_referenced_velocities(section_grid_file, section_data_file)                     # compute and write section rotated u,v in section model file
