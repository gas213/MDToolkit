from md_commands.command_interface import Command
from md_enums.atom_data_column_type import AtomDataColumnType
from session_state import SessionState

class AtomDataColumnCommand(Command):
    def __init__(self, column_type: AtomDataColumnType, column_index: int):
        self._column_type = column_type
        self._column_index = column_index
    
    def execute(self, state: SessionState):
        state.atom_data_columns[self._column_type] = self._column_index