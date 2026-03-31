from md_commands.command_interface import Command
from md_enums.aggregation_type import AggregationType
from md_operations.center_of_mass import calc_center_of_mass
from session_state import SessionState

class CenterOfMassCommand(Command):
    def __init__(self, aggregation_type: AggregationType):
        self._aggregation_type = aggregation_type

    def execute(self, state: SessionState):
        state.md_logger.log("Calculating center of mass...")
        com = calc_center_of_mass(state.atoms, state.atom_masses)
        if self._aggregation_type == AggregationType.NONE or state.center_of_mass is None:
            state.center_of_mass = com
        elif self._aggregation_type == AggregationType.AVERAGE:
            n_previous = state.data_files_index
            state.center_of_mass.x = (n_previous * state.center_of_mass.x + com.x) / (n_previous + 1)
            state.center_of_mass.y = (n_previous * state.center_of_mass.y + com.y) / (n_previous + 1)
            state.center_of_mass.z = (n_previous * state.center_of_mass.z + com.z) / (n_previous + 1)

        state.md_logger.log(f"Center of mass: {state.center_of_mass.x} {state.center_of_mass.y} {state.center_of_mass.z}") # TODO: remove