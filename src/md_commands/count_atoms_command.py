from md_commands.command_interface import Command
from md_commands.command_validation_helper import CommandValidationHelper
from md_domain.atom_count import AtomCount
from md_enums.aggregation_type import AggregationType
from session_state import SessionState

class CountAtomsCommand(Command):
    def __init__(self, command_name: str, args: list[str]):
        helper = CommandValidationHelper(command_name)
        helper.check_for_exact_arg_count(args, 3)
        self._filter_name = args[0]
        self._aggregation_type = helper.check_categorical_arg(args[1].lower(), AggregationType)
        self._write_path_relative = args[2]

    def execute(self, state: SessionState):
        state.md_logger.log(f"Counting atoms in filter group '{self._filter_name}'...")
        atoms = state.get_filtered_atoms(self._filter_name)
        if len(atoms) == 0:
            raise Exception(f"count_atoms command: filter group '{self._filter_name}' contains no atoms.")
        
        if self._write_path_relative not in state.analyses:
            atom_count = AtomCount(self._aggregation_type)
            state.analyses[self._write_path_relative] = atom_count
        else:
            atom_count = state.analyses[self._write_path_relative]
            if not isinstance(atom_count, AtomCount):
                raise Exception(f"Analysis with name '{self._write_path_relative}' already exists but is not an atom count analysis, cannot add data to it.")

        atom_count.add_data(state.step_current, len(atoms))