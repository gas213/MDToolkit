from md_commands.command_interface import Command
from md_commands.command_helpers import parse_float, parse_int
from session_state import SessionState

class AtomMassCommand(Command):
    _atom_type: int = None
    _atom_mass: float = None
    
    def __init__(self, atom_type: int, atom_mass: float):
        self._atom_type = atom_type
        self._atom_mass = atom_mass

    @classmethod
    def from_args(cls, args: list[str]):
        expected_arg_count: int = 2
        if len(args) != expected_arg_count:
            raise Exception(f"atom_mass command does not have the right number of args (expected {expected_arg_count}, got {len(args)})")
        return cls(parse_int(args[0]), parse_float(args[1]))
    
    def execute(self, state: SessionState):
        state.atom_masses[self._atom_type] = self._atom_mass