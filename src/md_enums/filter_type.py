from enum import Enum

class FilterType(Enum):
    ATOM_TYPE = "atom_type"
    CARTESIAN = "cartesian"
    CYLINDRICAL_Z = "cylindrical_z"
    INTERSECT = "intersect"
    MOL_NEIGHBORS = "mol_neighbors"
    NEIGHBOR_COUNT = "neighbor_count"
    SPHERICAL = "spherical"
    UNION = "union"