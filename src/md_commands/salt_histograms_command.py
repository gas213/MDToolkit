from file_writer import write_salt_histograms
from md_commands.command_interface import Command
from md_commands.command_validation_helper import CommandValidationHelper
from md_enums.aggregation_type import AggregationType
from md_operations.salt_histograms import build_salt_histograms
from session_state import SessionState

class SaltHistogramsCommand(Command):
    def __init__(self, command_name: str, args: list[str]):
        helper = CommandValidationHelper(command_name)
        helper.check_for_exact_arg_count(args, 6)
        self._filter_name = args[0]
        self._type_na = helper.parse_int(args[1])
        self._type_cl = helper.parse_int(args[2])
        self._r_threshold = helper.parse_float(args[3])
        self._aggregation_type = helper.check_categorical_arg(args[4].lower(), AggregationType)
        self._write_path_relative = args[5]

    def execute(self, state: SessionState):
        if self._type_na not in state.atom_masses:
            raise Exception(f"salt_histograms command: sodium type specified as {self._type_na} but there is no atom_mass entry for this.")
        if self._type_cl not in state.atom_masses:
            raise Exception(f"salt_histograms command: chlorine type specified as {self._type_cl} but there is no atom_mass entry for this.")
        state.md_logger.log("Building salt histograms...")
        filtered_atoms = state.get_filtered_atoms(self._filter_name)
        histogram_na_centric, histogram_cl_centric = build_salt_histograms(filtered_atoms, self._type_na, self._type_cl, self._r_threshold)
        if self._aggregation_type == AggregationType.NONE or state.get_data_file_index() == 0:
            state.histogram_na_centric = histogram_na_centric
            state.histogram_cl_centric = histogram_cl_centric
            write_salt_histograms(state, self._write_path_relative, True)
        elif self._aggregation_type == AggregationType.AVERAGE and state.histogram_na_centric is not None and state.histogram_cl_centric is not None:
            n_previous = state.get_data_file_index()
            for key in state.histogram_na_centric.data.keys():
                state.histogram_na_centric.data[key] = (n_previous * state.histogram_na_centric.data[key] + histogram_na_centric.data[key]) / (n_previous + 1)
            for key in state.histogram_cl_centric.data.keys():
                state.histogram_cl_centric.data[key] = (n_previous * state.histogram_cl_centric.data[key] + histogram_cl_centric.data[key]) / (n_previous + 1)
            write_salt_histograms(state, self._write_path_relative, False)