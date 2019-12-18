
# Script that reads in Sections objects from sections.csv and generates
# CDO gridfiles for each Section object.

import read_sections

sections_file = "sections.csv"
intervals = [10000.0, 50000.0]

# loop over resolutions, read in sections and write cdo gridfiles
for dx in intervals:
    sections = read_sections.read_sections(sections_file, dx)

    for s in sections:
        data_file = "data/{}_{}km.grd".format(s.name, int(dx/1000.0))
        s.write_gridfile(data_file)
