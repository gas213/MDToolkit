from md_commands.command_interface import Command
from md_commands.command_validation_helper import CommandValidationHelper
from md_domain.density_profile import DensityProfile
from md_enums.aggregation_type import AggregationType
from md_enums.cartesian_axis import CartesianAxis
from md_operations.cartesian_density_profile import build_cartesian_density_profile
from session_state import SessionState

class CartesianDensityProfileCommand(Command):
    def __init__(self, command_name: str, args: list[str]):
        helper = CommandValidationHelper(command_name)
        helper.check_for_exact_arg_count(args, 8)
        self._filter_name = args[0]
        self._aggregation_type = helper.check_categorical_arg(args[1].lower(), AggregationType)
        self._axis = helper.check_categorical_arg(args[2].lower(), CartesianAxis)
        self._bin_start = helper.parse_float_or_none(args[3])
        self._bin_stop = helper.parse_float_or_none(args[4])
        self._bin_step = helper.parse_float(args[5])
        self._normalization_density = helper.parse_float(args[6])
        self._write_path_relative = args[7]

    def execute(self, state: SessionState):
        state.md_logger.log("Building cartesian density profile...")
        if state.header is None:
            raise Exception("cartesian_density_profile command: box dimensions must be read from a data file header first.")
        
        bin_start: float = self._bin_start if self._bin_start is not None else getattr(state.header.box.lo, self._axis.value)
        bin_stop: float = self._bin_stop if self._bin_stop is not None else getattr(state.header.box.hi, self._axis.value)
        if bin_stop <= bin_start:
            raise Exception(f"cartesian_density_profile command: bin_stop value ({bin_stop}) must be greater than bin_start value ({bin_start}).")
        elif bin_stop - bin_start < self._bin_step:
            raise Exception(f"cartesian_density_profile command: bin_step value ({self._bin_step}) is too large for the specified bin_start and bin_stop values, resulting in zero bins.")

        cross_section_area: float = 1.0
        for axis in CartesianAxis:
            if axis != self._axis:
                cross_section_area *= getattr(state.header.box.hi, axis.value) - getattr(state.header.box.lo, axis.value)

        atoms = state.get_filtered_atoms(self._filter_name)
        if len(atoms) == 0:
            raise Exception(f"cartesian_density_profile command: filter group '{self._filter_name}' contains no atoms.")
        
        if self._write_path_relative not in state.analyses:
            density_profile = DensityProfile(self._aggregation_type)
            state.analyses[self._write_path_relative] = density_profile
        else:
            density_profile = state.analyses[self._write_path_relative]
            if not isinstance(density_profile, DensityProfile):
                raise Exception(f"Analysis with name '{self._write_path_relative}' already exists but is not a density profile, cannot add data to it.")
        
        density_profile.add_data(state.step_current, build_cartesian_density_profile(atoms, self._axis, bin_start, bin_stop, self._bin_step, state.atom_masses, self._normalization_density, cross_section_area))