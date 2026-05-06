from md_commands.command_interface import Command
from md_commands.command_validation_helper import CommandValidationHelper
from session_state import SessionState

class SetPathsCommand(Command):
    def __init__(self, command_name: str, args: list[str]):
        helper = CommandValidationHelper(command_name)
        helper.check_for_min_arg_count(args, 2)
        self._data_path = args[0]
        self._results_path = args[1] if len(args) > 1 else None

    def execute(self, state: SessionState):
        state.new_paths(self._data_path, self._results_path)