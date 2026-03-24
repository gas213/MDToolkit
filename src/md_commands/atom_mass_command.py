from md_commands.command_interface import Command
from session_state import SessionState

class AtomMassCommand(Command):
    def __init__(self, atom_type: int, atom_mass: float):
        self._atom_type = atom_type
        self._atom_mass = atom_mass
    
    def execute(self, state: SessionState):
        state.atom_masses[self._atom_type] = self._atom_mass