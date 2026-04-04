from file_writer import write_histogram
from md_commands.command_interface import Command
from md_commands.command_validation_helper import CommandValidationHelper
from md_enums.aggregation_type import AggregationType
from md_operations.salt_histograms import build_cl_neighbors_histogram, build_na_neighbors_histogram
from session_state import SessionState

class SaltHistogramsCommand(Command):
    def __init__(self, command_name: str, args: list[str]):
        helper = CommandValidationHelper(command_name)
        helper.check_for_exact_arg_count(args, 3)
        self._filter_name = args[0]
        self._aggregation_type = helper.check_categorical_arg(args[1].lower(), AggregationType)
        self._write_path_relative = args[2]

    def execute(self, state: SessionState):
        state.md_logger.log("Building salt histograms...")
        filtered_atoms = state.get_filtered_atoms(self._filter_name)
        cl_neighbors_histogram = build_cl_neighbors_histogram(filtered_atoms)
        na_neighbors_histogram = build_na_neighbors_histogram(filtered_atoms)
        if self._aggregation_type == AggregationType.NONE or state.data_files_index == 0:
            state.cl_neighbors_histogram = cl_neighbors_histogram
            state.na_neighbors_histogram = na_neighbors_histogram
            write_histogram(state, self._write_path_relative, True)
        elif self._aggregation_type == AggregationType.AVERAGE:
            n_previous = state.data_files_index
            for key in state.cl_neighbors_histogram.keys():
                state.cl_neighbors_histogram[key] = (n_previous * state.cl_neighbors_histogram[key] + cl_neighbors_histogram[key]) / (n_previous + 1)
            for key in state.na_neighbors_histogram.keys():
                state.na_neighbors_histogram[key] = (n_previous * state.na_neighbors_histogram[key] + na_neighbors_histogram[key]) / (n_previous + 1)
            write_histogram(state, self._write_path_relative, False)