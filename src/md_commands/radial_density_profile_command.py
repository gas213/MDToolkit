from md_commands.command_interface import Command
from md_commands.command_validation_helper import CommandValidationHelper
from md_domain.radial_density_profile import DensityProfile
from md_enums.aggregation_type import AggregationType
from md_operations.radial_density_profile import build_radial_density_profile
from session_state import SessionState

class RadialDensityProfileCommand(Command):
    def __init__(self, command_name: str, args: list[str]):
        helper = CommandValidationHelper(command_name)
        helper.check_for_exact_arg_count(args, 7)
        self._filter_name = args[0]
        self._aggregation_type = helper.check_categorical_arg(args[1].lower(), AggregationType)
        self._bin_start = helper.parse_float(args[2])
        self._bin_stop = helper.parse_float(args[3])
        self._bin_step = helper.parse_float(args[4])
        self._normalization_density = helper.parse_float(args[5])
        self._write_path_relative = args[6]

    def execute(self, state: SessionState):
        if state.center_of_mass is None: raise Exception("Center of mass must be calculated before building radial density profile")
        state.md_logger.log("Building radial density profile...")
        atoms = state.get_filtered_atoms(self._filter_name)
        if len(atoms) == 0:
            raise Exception(f"radial_density_profile command: filter group '{self._filter_name}' contains no atoms.")
        
        if self._write_path_relative not in state.analyses:
            density_profile = DensityProfile(self._aggregation_type)
            state.analyses[self._write_path_relative] = density_profile
        else:
            density_profile = state.analyses[self._write_path_relative]
            if not isinstance(density_profile, DensityProfile):
                raise Exception(f"Analysis with name '{self._write_path_relative}' already exists but is not a density profile, cannot add data to it.")
        
        density_profile.add_data(state.step_current, build_radial_density_profile(atoms, state.center_of_mass, self._bin_start, self._bin_stop, self._bin_step, state.atom_masses, self._normalization_density))