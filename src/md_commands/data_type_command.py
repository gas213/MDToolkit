from md_commands.command_interface import Command
from md_commands.command_validation_helper import CommandValidationHelper
from md_enums.data_file_type import DataFileType
from session_state import SessionState

class DataTypeCommand(Command):
    def __init__(self, command_name: str, args: list[str]):
        helper = CommandValidationHelper(command_name)
        helper.check_for_exact_arg_count(args, 1)
        self._data_file_type = helper.check_categorical_arg(args[0].lower(), DataFileType)
    
    def execute(self, state: SessionState):
        state.data_file_type = self._data_file_type