from md_commands.command_interface import Command
from md_commands.command_validation_helper import CommandValidationHelper
from session_state import SessionState

class NextFileCommand(Command):
    def __init__(self, command_name: str, args: list[str]):
        helper = CommandValidationHelper(command_name)
        helper.check_for_exact_arg_count(args, 0)

    def execute(self, state: SessionState):
        current_index: int = state.get_data_file_index()
        if current_index < len(state.data_files) - 1:
            state.step_current = list(state.data_files)[current_index + 1]
        else:
            state.is_finished = True