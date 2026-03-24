from md_commands.command_interface import Command
from session_state import SessionState

class StepStartCommand(Command):
    def __init__(self, step: int):
        self._step = step
    
    def execute(self, state: SessionState):
        state.step_start = self._step