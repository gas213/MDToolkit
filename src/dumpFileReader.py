import os.path
import re

# EXPLANATION OF REGEX COMPONENTS
# \d+               Positive integer
# -?\d+             Positive or negative integer
# -?\d+\.?\d+       Positive or negative number that must have decimal digits
# -?\d+(\.\d+)?     Positive or negative number that might have decimal digits
regexes = {
    "total atoms": "^ITEM: NUMBER OF ATOMS$",
    "box": "^ITEM: BOX BOUNDS.*$",
    "atoms section header": "^ITEM: ATOMS.*$",
    "atoms section entry": "^\d+ \d+ -?\d+\.?\d+ -?\d+\.?\d+ -?\d+\.?\d+$",
}

def read_header(path):
    smoke_test(path)
    
    results = {
        "total atoms": None,
        "box": {}
    }
    
    for axis in ["x", "y", "z"]:
        results["box"][axis + "lo"] = None
        results["box"][axis + "hi"] = None

    atoms_flag = False
    box_flag = None
    with open(path, "r") as data:
        for line in data:
            if atoms_flag:
                results["total atoms"] = int(line)
                atoms_flag = False
            elif box_flag is not None:
                box_vals = line.split()
                results["box"][box_flag + "lo"] = float(box_vals[0])
                results["box"][box_flag + "hi"] = float(box_vals[1])
                if box_flag == "x": box_flag = "y"
                elif box_flag == "y": box_flag = "z"
                else: box_flag = None
                continue
            elif re.search(regexes["total atoms"], line) is not None:
                atoms_flag = True
                continue
            elif re.search(regexes["box"], line) is not None:
                box_flag = "x"
                continue
            elif re.search(regexes["atoms section header"], line) is not None:
                # We're not in the header section anymore, so make sure all header values have been obtained
                if any(val is None for val in results.values()):
                    message = "ERROR Did not find config values for the following: "
                    keys_missing_data = []
                    for key, val in results.items():
                        if val is None:
                            keys_missing_data.append(key)
                    message += ", ".join(keys_missing_data)
                    raise Exception(message)
                else: return results

def read_atoms(path, box_sim, box_vapor):
    smoke_test(path)

    results = {
        "atom counter": 0,
        "vapor counter": 0,
        "atom extremes": {
            "x": None,
            "y": None,
            "z": None
        },
        "density profiles": {
            "x": {},
            "y": {},
            "z": {}
        }
    }

    for axis in ["x", "y", "z"]:
        for val in range(int(box_sim[axis + "lo"]), int(box_sim[axis + "hi"]) + 1): results["density profiles"][axis][val] = 0

    with open(path, "r") as data:
        atoms_section_reached = False
        for line in data:
            if not atoms_section_reached:
                if re.search(regexes["atoms section header"], line) is not None:
                    atoms_section_reached = True
                    continue
                else: continue
            elif re.search(regexes["atoms section entry"], line) is not None:
                results["atom counter"] += 1
                row = line.split()
                coords = {}
                index = 2 # Atom x, y, z coordinates are located in the 3rd, 4th and 5th columns of the data file

                for axis in ["x", "y", "z"]:
                    coords[axis] = float(row[index])

                    if results["atom extremes"][axis] is None:
                        results["atom extremes"][axis] = [coords[axis], coords[axis]]
                    else:
                        if coords[axis] < results["atom extremes"][axis][0]: results["atom extremes"][axis][0] = coords[axis]
                        if coords[axis] > results["atom extremes"][axis][1]: results["atom extremes"][axis][1] = coords[axis]

                    if int(coords[axis]) in results["density profiles"][axis]:
                        results["density profiles"][axis][int(coords[axis])] += 1

                    index += 1

                atom_type = int(row[1])
                if (atom_type == 6 and
                    coords["x"] >= box_vapor["xlo"] and coords["x"] < box_vapor["xhi"] and
                    coords["y"] >= box_vapor["ylo"] and coords["y"] < box_vapor["yhi"] and
                    coords["z"] >= box_vapor["zlo"] and coords["z"] < box_vapor["zhi"]):
                        results["vapor counter"] += 1

    return results

def smoke_test(path):
    if path is None:
        raise Exception("Path not provided")
    elif not os.path.isfile(path):
        raise Exception("No file was found at the specified path")