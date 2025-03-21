from dataclasses import dataclass

from md_dataclasses.vector3d import Vector3D

@dataclass
class Box:
    lo: Vector3D
    hi: Vector3D