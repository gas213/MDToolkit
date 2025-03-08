import re

from readers.check_path import check_path
from named_tuples import Header

def header_from_dump_txt(path):
    check_path(path)
    
    results = {
        "atom_count": None,
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
            elif re.search("^ITEM: NUMBER OF ATOMS$", line) is not None:
                atoms_flag = True
                continue
            elif re.search("^ITEM: BOX BOUNDS.*$", line) is not None:
                box_flag = "x"
                continue
            elif re.search("^ITEM: ATOMS.*$", line) is not None:
                # We're not in the header section anymore, so make sure all header values have been obtained
                if any(val is None for val in results.values()):
                    message = "ERROR Did not find config values for the following: "
                    keys_missing_data = []
                    for key, val in results.items():
                        if val is None:
                            keys_missing_data.append(key)
                    message += ", ".join(keys_missing_data)
                    raise Exception(message)
                else: return Header(results["atom_count"], results["box"]["xlo"], results["box"]["xhi"],
                                    results["box"]["ylo"], results["box"]["yhi"], results["box"]["zlo"], results["box"]["zhi"])