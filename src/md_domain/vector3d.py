from dataclasses import dataclass

@dataclass
class Vector3D:
    x: float
    y: float
    z: float

    def to_array(self) -> list[float]:
        return [self.x, self.y, self.z]

    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector3D(self.x * other, self.y * other, self.z * other)
        else:
            raise NotImplementedError("Vector3D multiplication currently only supports scalar values.")

    def __sub__(self, other):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __str__(self):
        return f"x {self.x}, y {self.y}, z {self.z}"