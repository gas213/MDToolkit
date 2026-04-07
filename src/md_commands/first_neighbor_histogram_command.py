from md_commands.command_interface import Command
from md_commands.command_validation_helper import CommandValidationHelper
from md_domain.first_neighbor_histogram import FirstNeighborHistogram
from md_enums.aggregation_type import AggregationType
from md_operations.first_neighbor_histogram import build_first_neighbor_histogram_data
from session_state import SessionState

class FirstNeighborHistogramCommand(Command):
    def __init__(self, command_name: str, args: list[str]):
        helper = CommandValidationHelper(command_name)
        helper.check_for_exact_arg_count(args, 5)
        self._filter_name_atoms_center = args[0]
        self._filter_name_atoms_neighbor = args[1]
        self._r_threshold = helper.parse_float(args[2])
        self._aggregation_type = helper.check_categorical_arg(args[3].lower(), AggregationType)
        self._write_path_relative = args[4]

    def execute(self, state: SessionState):
        state.md_logger.log("Building first neighbor histogram...")
        atoms_center = state.get_filtered_atoms(self._filter_name_atoms_center)
        atoms_neighbor = state.get_filtered_atoms(self._filter_name_atoms_neighbor)
        if len(atoms_center) == 0:
            raise Exception(f"first_neighbor_histogram command: filter group '{self._filter_name_atoms_center}' contains no atoms.")
        if len(atoms_neighbor) == 0:
            raise Exception(f"first_neighbor_histogram command: filter group '{self._filter_name_atoms_neighbor}' contains no atoms.")
        
        if self._write_path_relative not in state.analyses:
            first_neighbor_histogram = FirstNeighborHistogram(self._aggregation_type)
            state.analyses[self._write_path_relative] = first_neighbor_histogram
        else:
            first_neighbor_histogram = state.analyses[self._write_path_relative]
            if not isinstance(first_neighbor_histogram, FirstNeighborHistogram):
                raise Exception(f"Analysis with name '{self._write_path_relative}' already exists but is not a FirstNeighborHistogram, cannot add data to it.")
        
        first_neighbor_histogram.add_data(state.step_current, build_first_neighbor_histogram_data(atoms_center, atoms_neighbor, self._r_threshold))