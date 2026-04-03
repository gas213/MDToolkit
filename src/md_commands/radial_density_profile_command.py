from md_commands.command_interface import Command
from md_commands.command_validation_helper import CommandValidationHelper
from md_enums.aggregation_type import AggregationType
from md_operations.radial_density_profile import build_radial_density_profile
from session_state import SessionState

class RadialDensityProfileCommand(Command):
    def __init__(self, command_name: str, args: list[str]):
        helper = CommandValidationHelper(command_name)
        helper.check_for_exact_arg_count(args, 4)
        self._aggregation_type = helper.check_categorical_arg(args[0].lower(), AggregationType)
        self._bin_start = helper.parse_float(args[1])
        self._bin_stop = helper.parse_float(args[2])
        self._bin_step = helper.parse_float(args[3])

    def execute(self, state: SessionState):
        if state.center_of_mass is None: raise Exception("Center of mass must be calculated before building radial density profile")
        state.md_logger.log("Building radial density profile...")
        profile = build_radial_density_profile(state.atoms, state.center_of_mass, self._bin_start, self._bin_stop, self._bin_step)
        if self._aggregation_type == AggregationType.NONE or state.data_files_index == 0:
            state.radial_profile = profile
        elif self._aggregation_type == AggregationType.AVERAGE:
            n_previous = state.data_files_index
            for key in state.radial_profile.keys():
                state.radial_profile[key] = (n_previous * state.radial_profile[key] + profile[key]) / (n_previous + 1)