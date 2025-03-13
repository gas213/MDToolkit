from typing import NamedTuple

class Atom(NamedTuple):
    id: int
    type: int
    x: float
    y: float
    z: float

class Box(NamedTuple):
    xlo: float
    xhi: float
    ylo: float
    yhi: float
    zlo: float
    zhi: float

class DensityProfileGroup(NamedTuple):
    x: dict[int, int]
    y: dict[int, int]
    z: dict[int, int]

class Header(NamedTuple):
    atom_count: int
    box: Box

class Vector3D(NamedTuple):
    x: float
    y: float
    z: float