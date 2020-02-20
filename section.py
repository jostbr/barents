
import subprocess
import math_tools

class Section(object):
    """
    Class for representing a section spanning from a start to end lat,lon coordinates
    with lat,lon coordinates evenly spaced (in meters) inbetween. Has support for writing a CDO
    gridfile based on the objects attributes.

    Example usage:
    > s = Section("bso", 77.0, 20.0, 70.0, 20.0, 10000.0)
    > s.write_section("bso.grd")
    """

    def __init__(self, name, lat0, lon0, lat1, lon1, dx):
        """
        Constructor setting defining attributes for the section.

        Args:
            name (str)   : Name idenitifier of section
            lat0 (float) : Latitude of section start
            lon0 (float) : Latitude of section start
            lat1 (float) : Latitude of section start
            lon1 (float) : Latitude of section start
        """
        self.name = name
        self.lat0 = lat0
        self.lon0 = lon0
        self.lat1 = lat1
        self.lon1 = lon1
        self.dx = dx
        self.coors = self.compute_section()

    def compute_section(self):
        """Function that computes lat,lon coordinates between edge
        points with even spacing given by self.dx."""
        azimuth = math_tools.calculate_bearing(self.lat0, self.lon0, self.lat1, self.lon1)
        coors = math_tools.get_coordinates(self.dx, azimuth, self.lat0, self.lon0, self.lat1, self.lon1)
        return coors

    def write_section(self, filename):
        """
        Method that writes a gridfile for CDO specfying a section,
        i.e. giving lat,lon coordinates along the section.

        Args:
            coors (list)   : List of tuples (lat/lon) for points along section
            filename (str) : Filename of CDO gridfile (ASCII) to write to
        """
        num_points = len(self.coors)
        lats = " ".join([str(l[0]) for l in self.coors])
        lons = " ".join([str(l[1]) for l in self.coors])

        with open(filename, "w") as f:
            f.write("# CDO gridfile for section: {} ({}km resolution)\n\n".format(self.name, self.dx/1000.0))
            f.write("gridtype = curvilinear\n")
            f.write("gridsize = {}\n".format(num_points))
            f.write("xsize = {}\n".format(num_points))
            f.write("ysize = 1\n\n")
            f.write("# Longitudes\nxvals = {}\n\n".format(lons))
            f.write("# Latitudes\nyvals = {}\n".format(lats))

    def interpolate(self, cdo_file, input_file, output_file):
        """
        Method that uses 'cdo remapbil' to inteprolate the input file to the
        section specified by the CDO gridfile and writes the result to the output file.

        Args:
            cdo_file (str)    : Grid file to provide to CDO defining the section
            input_file (str)  : Filename of some model data to interpolate to the section
            output_file (str) : Filename for section-interpolated data
        """
        subprocess.call("module load cdo", shell=True)
        subprocess.call("cdo remapbil,{} {} {}".format(cdo_file, input_file, output_file), shell=True)
        subprocess.call("ncwa -O -a y {} {}".format(output_file, output_file), shell=True)  # delete singleton dim "y"

    def plot(self):
        """Method to plot section on a map."""
        raise NotImplementedError

def read_csv(filename, dx):
    """Function that reads in sections from csv-style file defining section objects.
    Example file:
    -------------------------------------
    name,lat0,lon0,lat1,lon1
    barents_sea_opening_1,68,20,76,18
    barents_sea_opening_2,76,18,79.4,14
    svalbard_fjl,79.4,14,80.5,60
    fjl_novaya_zemlya,80.5,60,76,60
    novaya_zemlya_russia,71,55,68,65
    greenland_iceland,68,-35,65,-20
    iceland_faroe,65,-20,62,-6.3
    faroe_shetland,62,-6.3,60.5,-1.2
    shetland_norway,60.5,-1.2,60,7
    fram_strait,81,-15,79.4,14
    mid_barents,76,18,76,60
    -------------------------------------

    Args:
        filename (str) : Filename of csv file
        dx (float)     : At what resolution (meters) to create section objects
    Returns:
        sections (list) : List of objects genereates from reading the csv file
    """
    with open(filename, "r") as f:
        sections = list()
        f.next()  # skip header

        # for each line, extract name and edge coordinates and create Section object
        for line in f:
            words = line.split(",")
            coors = [float(w) for w in words[1:]]  # lat0, lon0, lat1, lon1
            sections.append(section.Section(words[0], *coors, dx=dx))

    return sections

def generate_gridfiles(sections_def_file, resolutions, output_dir):
    """Script that reads in Sections objects from sections.csv and generates
    CDO gridfiles for each Section object for each resolution.

    Args:
        sections_def_file (str) : Filename of csv file defining sections
        resolutions (list)      : List of floats at what resolutions to create grid files for
        output_dir (str)        : Directory to store CDO output grid files
    """
    output_template = os.path.join(output_dir, "{}_{}km.grd")
    
    for dx in resolutions:
        sections = read_sections(sections_def_file, dx)

        for s in sections:
            data_file = output_template.format(s.name, int(dx/1000.0))
            s.write_gridfile(data_file)

if __name__ == "__main__":
    # example usage
    s = Section("bso", 77.0, 20.0, 70.0, 20.0, 10000.0)
    s.write_section("bso.grd")
