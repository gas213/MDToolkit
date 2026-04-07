from dataclasses import dataclass, field

from md_domain.analysis import Analysis
from md_enums.aggregation_type import AggregationType

@dataclass
class FirstNeighborHistogram(Analysis):
    data: dict[int, dict[int, float]] = field(default_factory=dict) # Key is step number

    def get_printable(self) -> str:
        output: str = ""
        if len(self.data) == 0:
            pass
        elif self.aggregation_type == AggregationType.AVERAGE:
            hist_average: dict[int, float] = {}
            normalizer: float = 1.0 / len(self.data)
            for histogram in self.data.values():
                for key, value in histogram.items():
                    if key not in hist_average:
                        hist_average[key] = 0.0
                    hist_average[key] += value
            for key in hist_average:
                hist_average[key] *= normalizer
            output = " ".join([str(val) for val in hist_average.values()])
        else:
            output = "\n".join([str(step) + " " + " ".join([str(val) for val in histogram.values()]) for step, histogram in self.data.items()])
        return output
    
    def add_data(self, step: int, data: dict[int, float]):
        self.data[step] = data