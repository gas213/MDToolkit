from dataclasses import dataclass, field

from md_domain.analysis import Analysis
from md_enums.aggregation_type import AggregationType

@dataclass
class DensityProfile(Analysis):
    data: dict[int, dict[float, float]] = field(default_factory=dict) # Key is step number

    def get_printable(self) -> str:
        output: str = ""
        if len(self.data) == 0:
            pass
        elif self.aggregation_type == AggregationType.AVERAGE:
            profile_average: dict[float, float] = {}
            fraction: float = 1.0 / len(self.data)
            for profile in self.data.values():
                for key, val in profile.items():
                    if key not in profile_average:
                        profile_average[key] = 0.0
                    profile_average[key] += val
            for key in profile_average:
                profile_average[key] *= fraction
            output = "\n".join([f"{key} {val}" for key, val in profile_average.items()])
        else:
            output = "\n\n".join([str(step) + "\n" + "\n".join([f"{key} {val}" for key, val in profile.items()]) for step, profile in self.data.items()])
        return output
    
    def add_data(self, step: int, data: dict[float, float]):
        self.data[step] = data