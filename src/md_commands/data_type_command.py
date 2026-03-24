from md_commands.command_interface import Command
from md_enums.data_file_type import DataFileType
from session_state import SessionState

class DataTypeCommand(Command):
    def __init__(self, data_file_type: DataFileType):
        self._data_file_type = data_file_type
    
    def execute(self, state: SessionState):
        state.data_file_type = self._data_file_type