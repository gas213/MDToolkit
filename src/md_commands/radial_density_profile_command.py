from md_commands.command_interface import Command
from md_enums.aggregation_type import AggregationType
from md_operations.radial_density_profile import build_radial_density_profile
from session_state import SessionState

class RadialDensityProfileCommand(Command):
    def __init__(self, aggregation_type: AggregationType, bin_start: float, bin_stop: float, bin_step: float):
        self._aggregation_type = aggregation_type
        self._bin_start = bin_start
        self._bin_stop = bin_stop
        self._bin_step = bin_step

    def execute(self, state: SessionState):
        if state.center_of_mass is None: raise Exception("Center of mass must be calculated before building radial density profile")
        print("Building radial density profile...")
        profile = build_radial_density_profile(state.atoms, state.center_of_mass, self._bin_start, self._bin_stop, self._bin_step)
        if self._aggregation_type == AggregationType.NONE or state.data_files_index == 0:
            state.radial_profile = profile
        elif self._aggregation_type == AggregationType.AVERAGE:
            n_previous = state.data_files_index
            for key in state.radial_profile.keys():
                state.radial_profile[key] = (n_previous * state.radial_profile[key] + profile[key]) / (n_previous + 1)