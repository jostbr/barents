
import section

def read_sections(filename, interval):
    """Function that reads in sections from csv-style file.
    Could use pandas to read, but manuallt for now."""
    with open(filename, "r") as f:
        sections = list()
        f.next()  # skip header

        # for each line, extract name and edge coordinates and create Section object
        for line in f:
            words = line.split(",")
            coors = [float(w) for w in words[1:]]  # lat0, lon0, lat1, lon1
            sections.append(section.Section(words[0], *coors, interval=interval))

    return sections
