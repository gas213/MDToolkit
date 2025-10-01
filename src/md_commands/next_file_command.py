from md_commands.command_interface import Command
from session_state import SessionState

class NextFileCommand(Command):
    @classmethod
    def from_args(cls, args: list[str]):
        expected_arg_count: int = 0
        if len(args) != expected_arg_count:
            raise Exception(f"next_file command does not have the right number of args (expected {expected_arg_count}, got {len(args)})")
        return cls()
    
    def execute(self, state: SessionState):
        state.data_files_index += 1