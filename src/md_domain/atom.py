from dataclasses import dataclass

from md_domain.vector3d import Vector3D

@dataclass
class Atom:
    id: int
    mol: int
    type: int
    pos: Vector3D