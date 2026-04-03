from md_commands.command_interface import Command
from md_commands.command_validation_helper import CommandValidationHelper
from session_state import SessionState

class AtomMassCommand(Command):
    def __init__(self, command_name: str, args: list[str]):
        helper = CommandValidationHelper(command_name)
        helper.check_for_exact_arg_count(args, 2)
        self._atom_type = helper.parse_int(args[0])
        self._atom_mass = helper.parse_float(args[1])

    def execute(self, state: SessionState):
        state.atom_masses[self._atom_type] = self._atom_mass