from md_commands.command_helpers import parse_float
from md_commands.command_interface import Command
from md_operations.radial_density_profile import build_radial_density_profile
from session_state import SessionState

class RadialDensityProfileCommand(Command):
    _keep_average: bool = None
    _bin_start: float = None
    _bin_stop: float = None
    _bin_step: float = None

    def __init__(self, keep_average: bool, bin_start: float, bin_stop: float, bin_step: float):
        self._keep_average = keep_average
        self._bin_start = bin_start
        self._bin_stop = bin_stop
        self._bin_step = bin_step

    @classmethod
    def from_args(cls, args: list[str]):
        expected_arg_count: int = 4
        if len(args) != expected_arg_count:
            raise Exception(f"radial_density_profile command does not have the right number of args (expected {expected_arg_count}, got {len(args)})")
        averaging_arg = args[0].lower()
        if averaging_arg == "overwrite":
            return cls(False, parse_float(args[1]), parse_float(args[2]), parse_float(args[3]))
        elif averaging_arg == "average":
            return cls(True, parse_float(args[1]), parse_float(args[2]), parse_float(args[3]))
        else:
            raise Exception(f"radial_density_profile command has invalid value for overwrite/average argument: {args[0]}")
    
    def execute(self, state: SessionState):
        print("Building radial density profile...")
        profile = build_radial_density_profile(state.atoms, state.center_of_mass, self._bin_start, self._bin_stop, self._bin_step)
        if not self._keep_average or state.data_files_index == 0:
            state.radial_profile = profile
        else:
            n_previous = state.data_files_index
            for key in state.radial_profile.keys():
                state.radial_profile[key] = (n_previous * state.radial_profile[key] + profile[key]) / (n_previous + 1)