
# Wrapper  around CDO calls to calculate fluxes across a section
# by using a CDO grid file

import os
import argparse
import subprocess
from netCDF4 import Dataset, num2date
import scipy as sp
import numpy as np
import matplotlib.pyplot as plt

# constants
density = 1025 # kg/m3
specific_heat_capacity = 3850 # kg/m3

def valid_path(path):
    """Function that validates if path exists."""
    if os.path.exists(path):
        return path
    else:
        raise argparse.ArgumentTypeError("Invalid path {}!".format(path))

# handle command line arguments
parser = argparse.ArgumentParser(description="Interpolate model data to lon/lat section")
parser.add_argument("data_file", type=valid_path, help="filename of section data file containing velocities, temperature, and salinity")
parser.add_argument("section_file", type=valid_path, help="filename of section gridfile containing section cell areas")
args = parser.parse_args()

# check variable name of temperature 

# call CDO command to tinterpolate model data to section

section_grid = Dataset(args.section_file,'r')
data_file = Dataset(args.data_file,'r')

time_nc = data_file.variables['time']
time = num2date(time_nc[:], time_nc.units)
cell_area = section_grid.variables['cell_area']
v = data_file_variables['v_sec']
temp = data_file.variables['temperature']


heat_flux = cell_area * np.sum(v, axis=(1,2)) * np.sum(temp, axis(1,2)) * density * specific_heat_capacity


# Calculate running 5-year mean
dt = time[1]-time[0]
N = 5*365*24*3600 / dt.total_seconds()
kernel = sp.ones(N)/N
heat_flux_5y = sp.convolve(heat_flux, kernel, mode='constant')


# plot 
fig = plt.figure(figsize=[12,8])
plt.plot(time, heat_flux_5y, lw=2, label='5 avg')
plt.plot(time, heat_flux, lw=1, label='instantanous')
plt.savefig('heatflux.png')


