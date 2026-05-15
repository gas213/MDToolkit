from dataclasses import dataclass, field

from md_domain.analysis import Analysis
from md_enums.aggregation_type import AggregationType

@dataclass
class AtomCount(Analysis):
    data: dict[int, int] = field(default_factory=dict) # Key is step number

    def get_printables(self) -> dict[str, str]:
        printables: dict[str, str] = {}
        if len(self.data) == 0:
            return printables
        if self.aggregation_type == AggregationType.AVERAGE or self.aggregation_type == AggregationType.BOTH:
            count_average: float = 0.0
            for count in self.data.values():
                count_average += count
            count_average /= float(len(self.data))
            printables["avg"] = f"{count_average}"
        if self.aggregation_type == AggregationType.RAW or self.aggregation_type == AggregationType.BOTH:
            printables["raw"] = "\n".join([f"{step} {count}" for step, count in self.data.items()])
        
        return printables

    def add_data(self, step: int, data: int) -> None:
        self.data[step] = data