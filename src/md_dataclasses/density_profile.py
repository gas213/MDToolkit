from dataclasses import dataclass

@dataclass
class DensityProfile:
    data: dict[str, float]
    description: str