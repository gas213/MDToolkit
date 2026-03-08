"""
Replaces the value of all RNG_* variables in a given LAMMPS input script.
"""

import os
import random
import re
import sys

TARGET_REGEX: str = r"^variable\s+rng_\S+\s+equal\s+([0-9]+)($|\s)"
DIGITS: int = 8

if __name__ == "__main__":
    # Only argument is the path to the input script
    if len(sys.argv) != 2:
        raise Exception(f"Expected exactly one argument, the path to the input script, but got {len(sys.argv)} arguments")
    in_path = sys.argv[1]
    if not os.path.exists(in_path):
        raise Exception(f"Input file does not exist: {in_path}")
    lines = []
    with open(in_path, "r") as file:
        for line in file:
            match = re.search(TARGET_REGEX, line.lower())
            if match:
                old_seed = match.group(1)
                new_seed = str(random.randint(0, 10**DIGITS) - 1).zfill(DIGITS)
                line = line.replace(old_seed, new_seed)
            lines.append(line)
    with open(in_path, "w") as file:
        file.writelines(lines)