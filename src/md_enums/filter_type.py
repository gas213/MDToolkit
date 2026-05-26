from enum import Enum

class FilterType(Enum):
    ATOM_TYPE = "atom_type"
    CARTESIAN = "cartesian"
    INTERSECT = "intersect"
    MOL_NEIGHBORS = "mol_neighbors"
    NEIGHBOR_COUNT = "neighbor_count"
    RADIAL = "radial"
    UNION = "union"