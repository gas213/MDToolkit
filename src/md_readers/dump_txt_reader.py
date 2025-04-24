import re

from md_dataclasses.atom import Atom
from md_dataclasses.box import Box
from md_dataclasses.header import Header
from md_dataclasses.vector3d import Vector3D
from md_readers.config_reader import ConfigReader

# EXPLANATION OF REGEX COMPONENTS
# \d+               Positive integer
# -?\d+             Positive or negative integer
# -?\d+\.?\d+       Positive or negative number that must have decimal digits
# -?\d+(\.\d+)?     Positive or negative number that might have decimal digits
regexes = {
    "atom count label": "^ITEM: NUMBER OF ATOMS$",
    "box label": "^ITEM: BOX BOUNDS.*$",
    "atoms header": "^ITEM: ATOMS.*$",
    "atoms record": "^\d+ \d+ -?\d+\.?\d+ -?\d+\.?\d+ -?\d+\.?\d+$"
}

def read_header(data_file: str) -> Header:    
    results = {
        "atom_count": None,
        "box": {}
    }
    
    for axis in ["x", "y", "z"]:
        results["box"][axis + "lo"] = None
        results["box"][axis + "hi"] = None

    atoms_flag = False
    box_flag = None
    with open(data_file, "r") as data:
        for line in data:
            if atoms_flag:
                results["atom_count"] = int(line)
                atoms_flag = False
            elif box_flag is not None:
                box_vals = line.split()
                results["box"][box_flag + "lo"] = float(box_vals[0])
                results["box"][box_flag + "hi"] = float(box_vals[1])
                if box_flag == "x": box_flag = "y"
                elif box_flag == "y": box_flag = "z"
                else: box_flag = None
                continue
            elif re.search(regexes["atom count label"], line) is not None:
                atoms_flag = True
                continue
            elif re.search(regexes["box label"], line) is not None:
                box_flag = "x"
                continue
            elif re.search(regexes["atoms header"], line) is not None:
                # We're not in the header section anymore, so make sure all header values have been obtained
                if any(val is None for val in results.values()):
                    message = "ERROR Did not find config values for the following: "
                    keys_missing_data = []
                    for key, val in results.items():
                        if val is None:
                            keys_missing_data.append(key)
                    message += ", ".join(keys_missing_data)
                    raise Exception(message)
                else: return Header(results["atom_count"], Box(Vector3D(results["box"]["xlo"], results["box"]["ylo"], results["box"]["zlo"]),
                                                               Vector3D(results["box"]["xhi"], results["box"]["yhi"], results["box"]["zhi"])))
                
def read_atoms(config: ConfigReader, data_file: str) -> list[Atom]:
    atoms = []
    with open(data_file, "r") as data:
        atoms_section_reached = False
        for line in data:
            if not atoms_section_reached:
                if re.search(regexes["atoms header"], line) is not None:
                    atoms_section_reached = True
                    continue
                else: continue
            elif re.search(regexes["atoms record"], line) is not None:
                row = line.split()
                id = int(row[config.data_columns["Id"]])
                type = int(row[config.data_columns["Type"]])
                x = float(row[config.data_columns["X"]])
                y = float(row[config.data_columns["Y"]])
                z = float(row[config.data_columns["Z"]])
                atoms.append(Atom(id, type, Vector3D(x, y, z)))

    return atoms