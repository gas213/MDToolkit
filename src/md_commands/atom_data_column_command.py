from md_commands.command_interface import Command
from md_commands.command_helpers import parse_int
from session_state import SessionState

_supported_atom_properties = [
    "id",
    "type",
    "x",
    "y",
    "z",
]

class AtomDataColumnCommand(Command):
    _atom_property: str = None
    _column_index: int = None
    
    def __init__(self, atom_property: str, column_index: int):
        self._atom_property = atom_property
        self._column_index = column_index

    @classmethod
    def from_args(cls, args: list[str]):
        expected_arg_count: int = 2
        if len(args) != expected_arg_count:
            raise Exception(f"atom_data_column command does not have the right number of args (expected {expected_arg_count}, got {len(args)})")
        atom_property = args[0].lower()
        if atom_property not in _supported_atom_properties:
            raise Exception(f"Unsupported atom_data_column property specified in configuration: '{atom_property}' (supported types are {_supported_atom_properties})")
        return cls(atom_property, parse_int(args[1]))
    
    def execute(self, state: SessionState):
        state.atom_data_columns[self._atom_property] = self._column_index