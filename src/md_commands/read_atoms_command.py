from md_commands.command_interface import Command
from md_commands.command_validation_helper import CommandValidationHelper
from md_data_readers import write_data_reader as writedata
from md_data_readers import dump_nc_reader as dumpnc
from md_data_readers import dump_txt_reader as dumptxt
from md_enums.atom_data_column_type import AtomDataColumnType
from md_enums.data_file_type import DataFileType
from session_state import SessionState

class ReadAtomsCommand(Command):
    def __init__(self, command_name: str, args: list[str]):
        helper = CommandValidationHelper(command_name)
        helper.check_for_exact_arg_count(args, 0)

    def execute(self, state: SessionState):
        data_file_name = state.data_files[state.step_current]
        state.md_logger.log(f"Reading atoms from data file {data_file_name}...")
        if state.data_file_type == DataFileType.DUMP_NETCDF:
            state.atoms = dumpnc.read_atoms(data_file_name)
            return
        for column_type in [AtomDataColumnType.ID, AtomDataColumnType.TYPE, AtomDataColumnType.X, AtomDataColumnType.Y, AtomDataColumnType.Z]:
            if column_type not in state.atom_data_columns:
                raise Exception(f"Missing atom_data_column command for '{column_type.value}' field; this is required in the input file.")
        if state.data_file_type == DataFileType.DUMP_TXT: state.atoms = dumptxt.read_atoms(data_file_name, state.atom_data_columns)
        elif state.data_file_type == DataFileType.WRITE_DATA: state.atoms = writedata.read_atoms(data_file_name, state.atom_data_columns)
        else: raise Exception(f"Invalid data_type in session state: {state.data_file_type}")
