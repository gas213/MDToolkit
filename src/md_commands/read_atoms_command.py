from md_commands.command_interface import Command
from md_data_readers import write_data_reader as writedata
from md_data_readers import dump_nc_reader as dumpnc
from md_data_readers import dump_txt_reader as dumptxt
from session_state import SessionState

class ReadAtomsCommand(Command):
    @classmethod
    def from_args(cls, args: list[str]):
        expected_arg_count: int = 0
        if len(args) != expected_arg_count:
            raise Exception(f"read_atoms command does not have the right number of args (expected {expected_arg_count}, got {len(args)})")
        return cls()
    
    def execute(self, state: SessionState):
        data_file_name = state.data_files[state.data_files_index]
        print(f"Reading atoms from data file {data_file_name}...")
        if state.data_type == "write_data": state.atoms = writedata.read_atoms(data_file_name, state.atom_data_columns)
        elif state.data_type == "dump_txt": state.atoms = dumptxt.read_atoms(data_file_name, state.atom_data_columns)
        elif state.data_type == "dump_netcdf": state.atoms = dumpnc.read_atoms(data_file_name)
        else: raise Exception(f"Invalid data_type in session state: {state.data_type}")
