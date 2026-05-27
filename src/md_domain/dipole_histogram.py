from dataclasses import dataclass, field

from md_domain.analysis import Analysis
from md_enums.aggregation_type import AggregationType

@dataclass
class DipoleHistogram(Analysis):
    data: dict[int, dict[float, float]] = field(default_factory=dict) # Key is step number

    def get_printables(self) -> dict[str, str]:
        printables: dict[str, str] = {}
        if len(self.data) == 0:
            return printables
        if self.aggregation_type == AggregationType.AVERAGE or self.aggregation_type == AggregationType.BOTH:
            histogram_average: dict[float, float] = {}
            fraction: float = 1.0 / len(self.data)
            for histogram in self.data.values():
                for key, val in histogram.items():
                    if key not in histogram_average:
                        histogram_average[key] = 0.0
                    histogram_average[key] += val
            for key in histogram_average:
                histogram_average[key] *= fraction
            printables["avg"] = "\n".join([f"{key} {val}" for key, val in histogram_average.items()])
        if self.aggregation_type == AggregationType.RAW or self.aggregation_type == AggregationType.BOTH:
            printables["raw"] = "\n\n".join([str(step) + "\n" + "\n".join([f"{key} {val}" for key, val in histogram.items()]) for step, histogram in self.data.items()])
        return printables

    def add_data(self, step: int, data: dict[float, float]) -> None:
        self.data[step] = data