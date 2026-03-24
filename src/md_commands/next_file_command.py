from md_commands.command_interface import Command
from session_state import SessionState

class NextFileCommand(Command):
    def execute(self, state: SessionState):
        state.data_files_index += 1