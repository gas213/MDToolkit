from abc import ABC, abstractmethod

from session_state import SessionState

class Command(ABC):
    @classmethod
    @abstractmethod
    def from_args(cls, args: list[str]):
        pass

    @abstractmethod
    def execute(self, state: SessionState):
        pass