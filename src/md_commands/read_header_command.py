from md_commands.command_interface import Command
from md_commands.command_validation_helper import CommandValidationHelper
from md_data_readers import write_data_reader as writedata
from md_data_readers import dump_nc_reader as dumpnc
from md_data_readers import dump_txt_reader as dumptxt
from md_enums.data_file_type import DataFileType
from session_state import SessionState

class ReadHeaderCommand(Command):
    def __init__(self, command_name: str, args: list[str]):
        helper = CommandValidationHelper(command_name)
        helper.check_for_exact_arg_count(args, 0)

    def execute(self, state: SessionState):
        data_file_name = list(state.data_files.values())[0]
        state.md_logger.log(f"Reading header fields of data file {data_file_name}...")
        if state.data_file_type == DataFileType.DUMP_NETCDF: state.header = dumpnc.read_header(data_file_name)
        elif state.data_file_type == DataFileType.DUMP_TXT: state.header = dumptxt.read_header(data_file_name)
        elif state.data_file_type == DataFileType.WRITE_DATA: state.header = writedata.read_header(data_file_name)
        else: raise Exception(f"Invalid data_type in session state: {data_file_name}")