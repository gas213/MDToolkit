import numpy as np
import re

from md_dataclasses.atom import Atom
from md_dataclasses.vector3d import Vector3D
from md_readers.check_path import check_path

# EXPLANATION OF REGEX COMPONENTS
# \d+               Positive integer
# -?\d+             Positive or negative integer
# -?\d+\.?\d+       Positive or negative number that must have decimal digits
# -?\d+(\.\d+)?     Positive or negative number that might have decimal digits
def atoms_from_dump_txt(path):
    check_path(path)

    atoms = []
    with open(path, "r") as data:
        atoms_section_reached = False
        for line in data:
            if not atoms_section_reached:
                if re.search("^ITEM: ATOMS.*$", line) is not None:
                    atoms_section_reached = True
                    continue
                else: continue
            elif re.search("^\d+ \d+ -?\d+\.?\d+ -?\d+\.?\d+ -?\d+\.?\d+$", line) is not None:
                row = line.split()
                atoms.append(Atom(int(row[0]), int(row[1]), Vector3D(float(row[2]), float(row[3]), float(row[4]))))

    # Adding and removing [None] is a trick to get the atom objects to retain their namedtuple field names during the array conversion
    # https://stackoverflow.com/a/53577004
    return np.array(atoms + [None], object)[:-1]