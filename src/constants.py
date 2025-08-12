import math
import os

# Atomic masses lookup table (should match the masses in the LAMMPS data file)
masses = {
    "C": 12.011,
    "Cl": 35.453,
    "F": 18.9984,
    "H": 1.008,
    "Na": 22.98977,
    "O": 15.9994,
}

# Sets of elements to build profiles for
element_sets = {
    # Individual elements
    "carbon": ["C"],
    "chlorine": ["Cl"],
    "fluorine": ["F"],
    "hydrogen": ["H"],
    "oxygen": ["O"],
    "sodium": ["Na"],
    # Groups of elements
    "all_element": ["All"],
    "ptfe": ["C", "F"],
    "salt": ["Cl", "Na"],
    "saltwater": ["Cl", "Na", "H", "O"],
    "water": ["H", "O"],
}

# For sphere volume calculation
four_thirds_pi = 4.0 * math.pi / 3.0

# Number of workers to use in multiprocessing pool
WORKER_COUNT: int = max(round(os.cpu_count() * 0.5), 1)

# Size of the x-y-z sampling bins, in angstroms
BIN_SIZE: float = 40.0