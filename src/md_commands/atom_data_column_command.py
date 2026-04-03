from md_commands.command_interface import Command
from md_commands.command_validation_helper import CommandValidationHelper
from md_enums.atom_data_column_type import AtomDataColumnType
from session_state import SessionState

class AtomDataColumnCommand(Command):
    def __init__(self, command_name: str, args: list[str]):
        helper = CommandValidationHelper(command_name)
        helper.check_for_exact_arg_count(args, 2)
        self._column_type = helper.check_categorical_arg(args[0].lower(), AtomDataColumnType)
        self._column_index = helper.parse_int(args[1])

    def execute(self, state: SessionState):
        state.atom_data_columns[self._column_type] = self._column_index