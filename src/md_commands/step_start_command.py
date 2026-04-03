from md_commands.command_interface import Command
from md_commands.command_validation_helper import CommandValidationHelper
from session_state import SessionState

class StepStartCommand(Command):
    def __init__(self, command_name: str, args: list[str]):
        helper = CommandValidationHelper(command_name)
        helper.check_for_exact_arg_count(args, 1)
        self._step = helper.parse_int(args[0])
    
    def execute(self, state: SessionState):
        state.step_start = self._step