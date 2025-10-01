from md_commands.command_interface import Command
from session_state import SessionState

_supported_data_types = [
    "write_data",
    "dump_txt",
    "dump_netcdf",
]

class DataTypeCommand(Command):
    _data_type: str = None

    def __init__(self, data_type: str):
        self._data_type = data_type

    @classmethod
    def from_args(cls, args: list[str]):
        expected_arg_count: int = 1
        if len(args) != expected_arg_count:
            raise Exception(f"data_type command does not have the right number of args (expected {expected_arg_count}, got {len(args)})")
        if args[0].lower() not in _supported_data_types:
            raise Exception(f"Unsupported data_type specified in configuration: '{args[0]}' (supported types are {_supported_data_types})")
        return cls(args[0])
    
    def execute(self, state: SessionState):
        state.data_type = self._data_type