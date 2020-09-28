
import subprocess

def ncks_variable_extract(var_list, from_file, to_file):
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

def ncks_copy_variable(var_name, from_file, to_file):
    """
    Method that copies a variable from one netcdf file and appends it
    to another file using ncks.

    Args:
        from_file (str) : Filename of file containing variable
        to_file (str)   : Filename of file to append variable to
        var_name (str)  : Name of variable to copy
    """
    subprocess.call("ncks -A -v {} {} {}".format(var_name, from_file, to_file), shell=True)
    print("ncks -A -v {} {} {}".format(var_name, from_file, to_file))
