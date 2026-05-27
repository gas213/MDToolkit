from md_commands.command_interface import Command
from md_commands.command_validation_helper import CommandValidationHelper
from md_domain.dipole_histogram import DipoleHistogram
from md_domain.vector3d import Vector3D
from md_enums.aggregation_type import AggregationType
from md_operations.dipole_histogram import build_dipole_histogram_data
from session_state import SessionState

class DipoleHistogramCommand(Command):
    def __init__(self, command_name: str, args: list[str]):
        helper = CommandValidationHelper(command_name)
        helper.check_for_exact_arg_count(args, 8)
        self._filter_name_o = args[0]
        self._filter_name_h = args[1]
        self._cx_str = args[2]
        self._cy_str = args[3]
        self._cz_str = args[4]
        self._aggregation_type = helper.check_categorical_arg(args[5].lower(), AggregationType)
        self._n_bins = helper.parse_positive_int(args[6])
        self._write_path_relative = args[7]

    def execute(self, state: SessionState):
        state.md_logger.log("Calculating water dipole histogram...")
        # If origin arg is strictly numeric, treat it as a coordinate; otherwise, treat it as an analysis path for an existing center of mass analysis
        try:
            cx = float(self._cx_str)
        except ValueError:
            cx = state.get_current_com(self._cx_str).x
        try:
            cy = float(self._cy_str)
        except ValueError:
            cy = state.get_current_com(self._cy_str).y
        try:
            cz = float(self._cz_str)
        except ValueError:
            cz = state.get_current_com(self._cz_str).z

        atoms_o = state.get_filtered_atoms(self._filter_name_o)
        atoms_h = state.get_filtered_atoms(self._filter_name_h)
        if len(atoms_o) == 0:
            raise Exception(f"dipole_histogram command: filter group '{self._filter_name_o}' contains no atoms.")
        if len(atoms_h) == 0:
            raise Exception(f"dipole_histogram command: filter group '{self._filter_name_h}' contains no atoms.")

        if self._write_path_relative not in state.analyses:
            dipole_dist = DipoleHistogram(self._aggregation_type)
            state.analyses[self._write_path_relative] = dipole_dist
        else:
            dipole_dist = state.analyses[self._write_path_relative]
            if not isinstance(dipole_dist, DipoleHistogram):
                raise Exception(f"Analysis with name '{self._write_path_relative}' already exists but is not a dipole_histogram analysis, cannot add data to it.")

        dipole_dist.add_data(state.step_current, build_dipole_histogram_data(atoms_o, atoms_h, Vector3D(cx, cy, cz), self._n_bins))