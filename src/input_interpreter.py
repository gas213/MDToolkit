from session_state import SessionState
from md_commands.atom_data_column_command import AtomDataColumnCommand
from md_commands.atom_mass_command import AtomMassCommand
from md_commands.center_of_mass_command import CenterOfMassCommand
from md_commands.command_interface import Command
from md_commands.data_path_command import DataPathCommand
from md_commands.data_type_command import DataTypeCommand
from md_commands.next_file_command import NextFileCommand
from md_commands.radial_density_profile_command import RadialDensityProfileCommand
from md_commands.read_atoms_command import ReadAtomsCommand
from md_commands.read_header_command import ReadHeaderCommand
from md_commands.step_end_command import StepEndCommand
from md_commands.step_start_command import StepStartCommand

commands_map: dict[str, Command] = {
    "atom_data_column": AtomDataColumnCommand,
    "atom_mass": AtomMassCommand,
    "center_of_mass": CenterOfMassCommand,
    "data_path": DataPathCommand,
    "data_type": DataTypeCommand,
    "next_file": NextFileCommand,
    "radial_density_profile": RadialDensityProfileCommand,
    "read_atoms": ReadAtomsCommand,
    "read_header": ReadHeaderCommand,
    "step_end": StepEndCommand,
    "step_start": StepStartCommand,
}

class InputInterpreter:
    _lines: list[str]
    _index: int = 0

    def __init__(self, input: list[str]):
        self._lines = []
        for line in input:
            if line.strip() == "": continue
            if line.startswith("#"): continue
            if line.startswith("-"): continue
            if line.startswith("="): continue
            self._lines.append(line)
        
    def run(self, state: SessionState):
        while self._index < len(self._lines):
            self.interpret_next(state)

    def interpret_next(self, state: SessionState):
        terms = self._lines[self._index].split()
        current_command = terms[0].lower()
        args = terms[1:] if len(terms) > 1 else []
        if current_command not in commands_map:
            raise Exception(f"Unsupported command: {current_command}")
        command: Command = commands_map[current_command].from_args(args)
        command.execute(state)
        
        if current_command == "next_file" and state.data_files_index < len(state.data_files):
            # Navigate back to the most recent read_atoms command if there are still more files to process
            while self._index >= 0:
                self._index -= 1
                if self._lines[self._index].split()[0].lower() == "read_atoms": break
            if self._index < 0: raise Exception("next_file command did not find a read_atoms command to navigate back to")
        else:
            self._index += 1