
# Wrapper  around CDO calls to interpolate model data to a defined section
# by using a CDO grid file

import os
import argparse
import subprocess

def valid_path(path):
    """Function that validates if path exists."""
    if os.path.exists(path):
        return path
    else:
        raise argparse.ArgumentTypeError("Invalid path {}!".format(path))

# handle command line arguments
parser = argparse.ArgumentParser(description="Interpolate model data to lon/lat section")
parser.add_argument("section_file", type=valid_path, help="filename of cdo gridfile defining the section")
parser.add_argument("model_file", type=valid_path, help="filename of model data file")
parser.add_argument("output_file", type=str, help="filename of generated output file")
args = parser.parse_args()

# call CDO command to tinterpolate model data to section
subprocess.call("module load cdo", shell=True)
subprocess.call("cdo remapbil,{} {} {}".format(args.section_file, args.model_file, args.output_file), shell=True)
