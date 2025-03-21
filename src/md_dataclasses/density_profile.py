from dataclasses import dataclass

@dataclass
class DensityProfileGroup:
    x: dict[int, int]
    y: dict[int, int]
    z: dict[int, int]
    r_count: dict[int, int]
    r_density: dict[int, float]
    r_density_norm: dict[int, float]