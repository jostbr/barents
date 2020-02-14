
# Wrapper  around CDO calls to calculate fluxes across a section
# by using a CDO grid file

import os
import argparse
import subprocess

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
parser.add_argument("output_file", type=str, help="filename of generated output file")
args = parser.parse_args()

# check variable name of temperature 

# call CDO command to tinterpolate model data to section
subprocess.call("module load cdo", shell=True)
subprocess.call("ncks -a -v cell_area {} {}".format(args.section_file, args.data_file), shell=True)
subprocess.call("cdo expr,´volume_flux=cell_area*v_secs;heat_flux=volume_flux*temperature*{}*{}´ {} {}".format(specific_heat_capacity, density, args.data_file, args.output_file), shell=True)
#subprocess.call("nco 
