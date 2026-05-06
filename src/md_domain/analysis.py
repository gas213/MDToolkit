from abc import ABC, abstractmethod
from dataclasses import dataclass

from md_enums.aggregation_type import AggregationType

@dataclass
class Analysis(ABC):
    aggregation_type: AggregationType

    @abstractmethod
    def get_printables(self) -> dict[str, str]:
        pass