from abc import ABC, abstractmethod

from session_state import SessionState

class Command(ABC):
    @abstractmethod
    def execute(self, state: SessionState):
        pass