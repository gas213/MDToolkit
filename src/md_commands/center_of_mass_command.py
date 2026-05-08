from md_commands.command_interface import Command
from md_commands.command_validation_helper import CommandValidationHelper
from md_domain.center_of_mass import CenterOfMass
from md_enums.aggregation_type import AggregationType
from md_operations.center_of_mass import calc_center_of_mass
from session_state import SessionState

class CenterOfMassCommand(Command):
    def __init__(self, command_name: str, args: list[str]):
        helper = CommandValidationHelper(command_name)
        helper.check_for_exact_arg_count(args, 3)
        self._filter_name = args[0]
        self._aggregation_type = helper.check_categorical_arg(args[1].lower(), AggregationType)
        self._write_path_relative = args[2]

    def execute(self, state: SessionState):
        state.md_logger.log("Calculating center of mass...")
        atoms = state.get_filtered_atoms(self._filter_name)
        if len(atoms) == 0:
            raise Exception(f"center_of_mass command: filter group '{self._filter_name}' contains no atoms.")
        
        if self._write_path_relative not in state.analyses:
            com = CenterOfMass(self._aggregation_type)
            state.analyses[self._write_path_relative] = com
        else:
            com = state.analyses[self._write_path_relative]
            if not isinstance(com, CenterOfMass):
                raise Exception(f"Analysis with name '{self._write_path_relative}' already exists but is not a center_of_mass analysis, cannot add data to it.")

        com.add_data(state.step_current, calc_center_of_mass(atoms, state.atom_masses))