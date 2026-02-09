from md_commands.command_interface import Command
from md_operations.salt_histograms import build_cl_neighbors_histogram, build_na_neighbors_histogram
from session_state import SessionState

class SaltHistogramsCommand(Command):
    _filter_name: str = None
    _keep_average: bool = None

    def __init__(self, filter_name: str, keep_average: bool):
        self._filter_name = filter_name
        self._keep_average = keep_average

    @classmethod
    def from_args(cls, args: list[str]):
        expected_arg_count: int = 2
        if len(args) != expected_arg_count:
            raise Exception(f"salt_histograms command does not have the right number of args (expected {expected_arg_count}, got {len(args)})")
        averaging_arg = args[1].lower()
        if averaging_arg == "overwrite":
            return cls(args[0], False)
        elif averaging_arg == "average":
            return cls(args[0], True)
        else:
            raise Exception(f"salt_histograms command has invalid value for overwrite/average argument: {args[0]}")
    
    def execute(self, state: SessionState):
        if self._filter_name.lower() != "all" and self._filter_name not in state.filters:
            raise Exception(f"Filter name specified in salt_histograms command not found: {self._filter_name}")
        state.logger.debug("Building salt histograms...")
        if self._filter_name.lower() == "all":
            filtered_atoms = state.atoms
        else:
            filtered_atoms = state.filters[self._filter_name].apply(state.atoms)
        cl_neighbors_histogram = build_cl_neighbors_histogram(filtered_atoms)
        na_neighbors_histogram = build_na_neighbors_histogram(filtered_atoms)
        if not self._keep_average or state.data_files_index == 0:
            state.cl_neighbors_histogram = cl_neighbors_histogram
            state.na_neighbors_histogram = na_neighbors_histogram
        else:
            n_previous = state.data_files_index
            for key in state.cl_neighbors_histogram.keys():
                state.cl_neighbors_histogram[key] = (n_previous * state.cl_neighbors_histogram[key] + cl_neighbors_histogram[key]) / (n_previous + 1)
            for key in state.na_neighbors_histogram.keys():
                state.na_neighbors_histogram[key] = (n_previous * state.na_neighbors_histogram[key] + na_neighbors_histogram[key]) / (n_previous + 1)

        print("Cl neighbors histogram:\n" + str(state.cl_neighbors_histogram)) # TODO: remove
        print("Cl neighbors values only:\n" + "\n".join([str(val) for val in state.cl_neighbors_histogram.values()])) # TODO: remove
        print("Na neighbors histogram:\n" + str(state.na_neighbors_histogram)) # TODO: remove
        print("Na neighbors values only:\n" + "\n".join([str(val) for val in state.na_neighbors_histogram.values()])) # TODO: remove