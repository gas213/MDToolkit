from dataclasses import dataclass

@dataclass
class DensityProfile:
    data: dict[int, float]
    description: str