from dataclasses import dataclass, field

from md_domain.analysis import Analysis
from md_domain.vector3d import Vector3D
from md_enums.aggregation_type import AggregationType

@dataclass
class CenterOfMass(Analysis):
    data: dict[int, Vector3D] = field(default_factory=dict) # Key is step number

    def get_printables(self) -> dict[str, str]:
        printables: dict[str, str] = {}
        if len(self.data) == 0:
            return printables
        if self.aggregation_type == AggregationType.AVERAGE or self.aggregation_type == AggregationType.BOTH:
            com_average: Vector3D = Vector3D(0.0, 0.0, 0.0)
            fraction: float = 1.0 / len(self.data)
            for com in self.data.values():
                com_average.x += com.x
                com_average.y += com.y
                com_average.z += com.z
            com_average.x *= fraction
            com_average.y *= fraction
            com_average.z *= fraction
            printables["avg"] = f"{com_average.x} {com_average.y} {com_average.z}"
        if self.aggregation_type == AggregationType.RAW or self.aggregation_type == AggregationType.BOTH:
            printables["raw"] = "\n".join([str(step) + " " + f"{com.x} {com.y} {com.z}" for step, com in self.data.items()])
        
        return printables

    def add_data(self, step: int, data: Vector3D):
        self.data[step] = data