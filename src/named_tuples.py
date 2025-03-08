from typing import NamedTuple

class Atom(NamedTuple):
    id: int
    type: int
    x: float
    y: float
    z: float

class Header(NamedTuple):
    atom_count: int
    xlo: float
    xhi: float
    ylo: float
    yhi: float
    zlo: float
    zhi: float