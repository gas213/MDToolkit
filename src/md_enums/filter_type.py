from enum import Enum

class FilterType(Enum):
    ATOM_TYPE = "atom_type"
    CARTESIAN = "cartesian"
    INTERSECT = "intersect"
    RADIAL = "radial"