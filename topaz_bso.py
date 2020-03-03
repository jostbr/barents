
import netCDF4
import numpy as np
import section_grid
import math_tools

topaz_file = "https://thredds.met.no/thredds/dodsC/myocean/arc-mfc/ran-arc-myoceanv2/topaz_V4_myocean_arctic_grid1to8_da_class1_20181215.nc"
topaz_aggr_file = "https://thredds.met.no/thredds/dodsC/topaz/dataset-ran-arc-myoceanv2-be"
topaz_data_file = "test.nc"
cdo_grid_file = "bso.grd"
grid_file = "topaz_grid.nc"
section_grid_file = "topaz_grid_bso.nc"
section_data_file = "topaz_data_bso.nc"

st = section_grid.SectionGrid("bso", 68.0, 20.0, 76.0, 18.0, 10000.0)
st.write_section(cdo_grid_file)
st.generate_gridfile(["stereographic", "depth", "model_depth"], topaz_data_file, grid_file)
st.write_xymesh(grid_file, "x", "y", "x_mesh", "y_mesh")
st.interpolate(cdo_grid_file, grid_file, section_grid_file)
st.write_angle(section_grid_file, "x_mesh", "y_mesh", "angle")
st.copy_variable("depth", grid_file, section_grid_file)

# read depth levels and model depth from section grid file
ds = netCDF4.Dataset(section_grid_file, mode="r")
depth = ds.variables["depth"][:].copy()
model_depth = ds.variables["model_depth"][:].copy()
ds.close()

dz = math_tools.compute_dz(depth, model_depth)
st.write_area(section_grid_file, dz, "cell_area")

#print(dz*st.dx)
#area = st.compute_area(depth, model_depth)
#print(area)

# interpolate model data file to section
#st.interpolate(cdo_grid_file, topaz_data_file, section_data_file)
