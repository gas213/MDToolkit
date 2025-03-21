from dataclasses import dataclass

@dataclass
class Vector3D:
    x: float
    y: float
    z: float

    def __str__(self):
        return f"x {self.x}, y {self.y}, z {self.z}"