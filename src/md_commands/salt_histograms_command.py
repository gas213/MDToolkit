from md_commands.command_interface import Command
from md_enums.aggregation_type import AggregationType
from md_operations.salt_histograms import build_cl_neighbors_histogram, build_na_neighbors_histogram
from session_state import SessionState

class SaltHistogramsCommand(Command):
    def __init__(self, filter_name: str, aggregation_type: AggregationType):
        self._filter_name = filter_name
        self._aggregation_type = aggregation_type

    #TODO: Do parameter parsing and validation somewhere else, like in CommandFactory
    def execute(self, state: SessionState):
        if self._filter_name.lower() != "all" and self._filter_name not in state.filters:
            raise Exception(f"Filter name specified in salt_histograms command not found: {self._filter_name}")
        state.md_logger.log("Building salt histograms...")
        if self._filter_name.lower() == "all":
            filtered_atoms = state.atoms
        else:
            filtered_atoms = state.filters[self._filter_name].apply(state.atoms)
        cl_neighbors_histogram = build_cl_neighbors_histogram(filtered_atoms)
        na_neighbors_histogram = build_na_neighbors_histogram(filtered_atoms)
        if self._aggregation_type == AggregationType.NONE or state.data_files_index == 0:
            state.cl_neighbors_histogram = cl_neighbors_histogram
            state.na_neighbors_histogram = na_neighbors_histogram
        elif self._aggregation_type == AggregationType.AVERAGE:
            n_previous = state.data_files_index
            for key in state.cl_neighbors_histogram.keys():
                state.cl_neighbors_histogram[key] = (n_previous * state.cl_neighbors_histogram[key] + cl_neighbors_histogram[key]) / (n_previous + 1)
            for key in state.na_neighbors_histogram.keys():
                state.na_neighbors_histogram[key] = (n_previous * state.na_neighbors_histogram[key] + na_neighbors_histogram[key]) / (n_previous + 1)

        state.md_logger.log("Cl neighbors histogram:\n" + str(state.cl_neighbors_histogram)) # TODO: remove
        state.md_logger.log("Na neighbors histogram:\n" + str(state.na_neighbors_histogram)) # TODO: remove
        state.md_logger.log("Cl neighbors values only:\n" + " ".join([str(val) for val in state.cl_neighbors_histogram.values()])) # TODO: remove
        state.md_logger.log("Na neighbors values only:\n" + " ".join([str(val) for val in state.na_neighbors_histogram.values()])) # TODO: remove