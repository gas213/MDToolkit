import math
import os.path
import re

# EXPLANATION OF REGEX COMPONENTS
# \d+               Positive integer
# -?\d+             Positive or negative integer
# -?\d+\.?\d+       Positive or negative number that must have decimal digits
# -?\d+(\.\d+)?     Positive or negative number that might have decimal digits
regexes = {
    "total atoms": "^\d+ atoms$",
    "box x": "^-?\d+(\.\d+)? -?\d+(\.\d+)? xlo xhi$",
    "box y": "^-?\d+(\.\d+)? -?\d+(\.\d+)? ylo yhi$",
    "box z": "^-?\d+(\.\d+)? -?\d+(\.\d+)? zlo zhi$",
    "atoms section header": "^Atoms.*$",
    "atoms section entry": "^\d+ \d+ \d+ -?\d+(\.\d+)? -?\d+(\.\d+)? -?\d+(\.\d+)? -?\d+(\.\d+)? -?\d+ -?\d+ -?\d+$",
    "velocities section header": "^Velocities.*$"
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

    with open(path, "r") as data:
        for line in data:
            if re.search(regexes["total atoms"], line) is not None:
                results["total atoms"] = int(line.split()[0])
            elif re.search(regexes["box x"], line) is not None:
                row = line.split()
                results["box"]["xlo"] = float(row[0])
                results["box"]["xhi"] = float(row[1])
            elif re.search(regexes["box y"], line) is not None:
                row = line.split()
                results["box"]["ylo"] = float(row[0])
                results["box"]["yhi"] = float(row[1])
            elif re.search(regexes["box z"], line) is not None:
                row = line.split()
                results["box"]["zlo"] = float(row[0])
                results["box"]["zhi"] = float(row[1])
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

def read_atoms(path, box_sim, sphere_vapor):
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
                index = 4 # Atom x, y, z coordinates are located in the 5th, 6th and 7th columns of the data file

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

                if (int(row[2]) == 6): # Atom type == oxygen (saline data)
                    distance_r = 0.0
                    for axis in ["x", "y", "z"]:
                        distance_r += (coords[axis] - sphere_vapor[axis])**2
                    distance_r = math.sqrt(distance_r)
                    if (distance_r > sphere_vapor["r"]): results["vapor counter"] += 1

            elif re.search(regexes["velocities section header"], line) is not None:
                break

    return results

def smoke_test(path):
    if path is None:
        raise Exception("Path not provided")
    elif not os.path.isfile(path):
        raise Exception("No file was found at the specified path")