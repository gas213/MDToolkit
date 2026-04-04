import os.path

from session_state import SessionState

def write_histogram(state: SessionState, write_path_relative: str, append_flag: bool):
    check_results_path(state)
    write_path_full: str = os.path.join(str(state.results_path), write_path_relative)
    os.makedirs(os.path.dirname(write_path_full), exist_ok=True)
    write_mode: str = "a" if append_flag else "w"
    is_appending: bool = append_flag and os.path.isfile(write_path_full)

    with open(write_path_full, write_mode) as file:
        if is_appending:
            file.write("\n\n")
        file.write("Cl neighbors histogram, values only:\n" + " ".join([str(val) for val in state.cl_neighbors_histogram.values()]))
        file.write("\n\nNa neighbors histogram, values only:\n" + " ".join([str(val) for val in state.na_neighbors_histogram.values()]))

def check_results_path(state: SessionState):
    if state.results_path is None or not os.path.isdir(state.results_path):
        raise Exception("Cannot write analysis files before results path has been set.")