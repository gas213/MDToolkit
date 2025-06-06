from dataclasses import dataclass

from md_dataclasses.vector3d import Vector3D

@dataclass
class Atom:
    id: int
    type: int
    pos: Vector3D
    is_vapor: bool = False