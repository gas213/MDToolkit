from md_commands.command_interface import Command
from md_operations.center_of_mass import calc_center_of_mass
from session_state import SessionState

class CenterOfMassCommand(Command):
    _keep_average: bool = None

    def __init__(self, keep_average: bool):
        self._keep_average = keep_average

    @classmethod
    def from_args(cls, args: list[str]):
        expected_arg_count: int = 1
        if len(args) != expected_arg_count:
            raise Exception(f"center_of_mass command does not have the right number of args (expected {expected_arg_count}, got {len(args)})")
        averaging_arg = args[0].lower()
        if averaging_arg == "overwrite":
            return cls(False)
        elif averaging_arg == "average":
            return cls(True)
        else:
            raise Exception(f"center_of_mass command has invalid value for overwrite/average argument: {args[0]}")
    
    def execute(self, state: SessionState):
        print("Calculating center of mass...")
        com = calc_center_of_mass(state.atoms, state.atom_masses)
        if not self._keep_average or state.data_files_index == 0:
            state.center_of_mass = com
        else:
            n_previous = state.data_files_index
            state.center_of_mass.x = (n_previous * state.center_of_mass.x + com.x) / (n_previous + 1)
            state.center_of_mass.y = (n_previous * state.center_of_mass.y + com.y) / (n_previous + 1)
            state.center_of_mass.z = (n_previous * state.center_of_mass.z + com.z) / (n_previous + 1)