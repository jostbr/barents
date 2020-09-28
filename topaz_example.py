
# generic modules
import numpy as np

# module specific to this project
import section
import grid_file
import section_grid
import section_model
import math_tools
import misc_tools

# define filenames
#topaz_file = "https://thredds.met.no/thredds/dodsC/myocean/arc-mfc/ran-arc-myoceanv2/topaz_V4_myocean_arctic_grid1to8_da_class1_20181215.nc"
#topaz_aggr_file = "https://thredds.met.no/thredds/dodsC/topaz/dataset-ran-arc-myoceanv2-be"
topaz_data_file = "test.nc"
cdo_grid_file = "bso.grd"
topaz_grid_file = "topaz_grid.nc"
section_grid_file = "topaz_grid_bso.nc"
section_model_file = "topaz_data_bso.nc"

# make grid file object and compute angle between north and model y direction
misc_tools.ncks_variable_extract(["stereographic", "depth", "model_depth"], topaz_data_file, topaz_grid_file)  # create full domain gridfile from existing model data
gf = grid_file.GridFile(topaz_grid_file)
gf.write_angle("angle")                                                     # write angle to grid file

# create section
s = section.Section("bso", 68.0, 20.0, 76.0, 18.0, 50000.0)
s.write_section(cdo_grid_file)                                              # write section

# write section grid file
sg = section_grid.SectionGridFile(s, section_grid_file)
sg.interpolate(topaz_grid_file)                                             # interpolate topaz full grid file onto section
misc_tools.ncks_copy_variable("depth", topaz_grid_file, section_grid_file)  # copy depth from full gridfile to section gridfile
sg.write_area("depth", "model_depth", "cell_area")                          # compute area of cells along section (for use in transport computations)

# interpolate model data onto section and rotate velocities
st = section_model.SectionModelFile(s, section_model_file)
st.set_section_grid(section_grid_file)
st.interpolate(topaz_data_file)                                             # interpolate model data file to section
st.write_section_referenced_velocities()                                    # compute and write section rotated u,v in section model file
