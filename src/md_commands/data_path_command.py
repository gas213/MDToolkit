from md_commands.command_interface import Command
from md_operations.get_data_files import get_data_files
from session_state import SessionState

class DataPathCommand(Command):
    _path: str = None

    def __init__(self, path: str):
        self._path = path

    @classmethod
    def from_args(cls, args: list[str]):
        expected_arg_count: int = 1
        if len(args) != expected_arg_count:
            raise Exception(f"data_path command does not have the right number of args (expected {expected_arg_count}, got {len(args)})")
        return cls(args[0])
    
    def execute(self, state: SessionState):
        state.data_files = get_data_files(self._path, state.step_start, state.step_end)
        state.data_path = self._path