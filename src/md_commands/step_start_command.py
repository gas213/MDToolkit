from md_commands.command_interface import Command
from md_commands.command_helpers import parse_int
from session_state import SessionState

class StepStartCommand(Command):
    _step: int = None
    
    def __init__(self, step: int):
        self._step = step

    @classmethod
    def from_args(cls, args: list[str]):
        expected_arg_count: int = 1
        if len(args) != expected_arg_count:
            raise Exception(f"step_start command does not have the right number of args (expected {expected_arg_count}, got {len(args)})")
        return cls(parse_int(args[0]))
    
    def execute(self, state: SessionState):
        state.step_start = self._step