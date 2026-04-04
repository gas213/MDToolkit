from dataclasses import dataclass

from md_enums.salt_type import SaltType

@dataclass
class SaltHistogram:
    center_type: SaltType
    data: dict[int, float]

    def get_printable(self) -> str:
        return f"Salt histogram, {self.center_type.value}-centric, values only:\n" + " ".join([str(val) for val in self.data.values()])