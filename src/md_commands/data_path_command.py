from md_commands.command_interface import Command
from md_commands.command_validation_helper import CommandValidationHelper
from md_operations.get_data_files import get_data_files
from md_operations.make_initial_dirs import make_initial_dirs
from session_state import SessionState

class DataPathCommand(Command):
    def __init__(self, command_name: str, args: list[str]):
        helper = CommandValidationHelper(command_name)
        helper.check_for_exact_arg_count(args, 1)
        self._path = args[0]

    def execute(self, state: SessionState):
        state.data_files = get_data_files(self._path, state.step_start, state.step_end)
        state.data_path = self._path
        results_path = make_initial_dirs(self._path, state.step_start, state.step_end)
        state.set_results_path(results_path)