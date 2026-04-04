from abc import ABC, abstractmethod

from md_domain.atom import Atom

class Filter(ABC):
    @abstractmethod
    def apply(self, atoms: list[Atom]) -> list[Atom]:
        pass