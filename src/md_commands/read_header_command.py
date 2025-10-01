from md_commands.command_interface import Command
from md_data_readers import write_data_reader as writedata
from md_data_readers import dump_nc_reader as dumpnc
from md_data_readers import dump_txt_reader as dumptxt
from session_state import SessionState

class ReadHeaderCommand(Command):
    @classmethod
    def from_args(cls, args: list[str]):
        expected_arg_count: int = 0
        if len(args) != expected_arg_count:
            raise Exception(f"read_header command does not have the right number of args (expected {expected_arg_count}, got {len(args)})")
        return cls()
    
    def execute(self, state: SessionState):
        data_file_name = state.data_files[0]
        print(f"Reading header fields of data file {data_file_name}...")
        if state.data_type == "write_data": state.header = writedata.read_header(data_file_name)
        elif state.data_type == "dump_txt": state.header = dumptxt.read_header(data_file_name)
        elif state.data_type == "dump_netcdf": state.header = dumpnc.read_header(data_file_name)
        else: raise Exception(f"Invalid data_type in session state: {data_file_name}")