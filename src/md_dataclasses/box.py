from dataclasses import dataclass

from md_dataclasses.vector3d import Vector3D

@dataclass
class Box:
    lo: Vector3D
    hi: Vector3D

    def __str__(self):
        return f"xlo {self.lo.x}, xhi {self.hi.x}, ylo {self.lo.y}, yhi {self.hi.y}, zlo {self.lo.z}, zhi {self.hi.z}"