from md_commands.command_interface import Command
from session_state import SessionState

class StepEndCommand(Command):
    def __init__(self, step: int):
        self._step = step
    
    def execute(self, state: SessionState):
        state.step_end = self._step