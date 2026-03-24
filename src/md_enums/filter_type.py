from enum import Enum

class FilterType(Enum):
    AND = "and"
    ATOM_TYPE = "atom_type"
    CARTESIAN = "cartesian"
    RADIAL = "radial"