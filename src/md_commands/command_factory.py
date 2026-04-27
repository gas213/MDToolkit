from md_commands.atom_data_column_command import AtomDataColumnCommand
from md_commands.atom_mass_command import AtomMassCommand
from md_commands.cartesian_density_profile_command import CartesianDensityProfileCommand
from md_commands.center_of_mass_command import CenterOfMassCommand
from md_commands.command_interface import Command
from md_commands.data_path_command import DataPathCommand
from md_commands.data_type_command import DataTypeCommand
from md_commands.filter_command import FilterCommand
from md_commands.first_neighbor_histogram_command import FirstNeighborHistogramCommand
from md_commands.next_file_command import NextFileCommand
from md_commands.radial_density_profile_command import RadialDensityProfileCommand
from md_commands.read_file_command import ReadFileCommand
from md_commands.step_end_command import StepEndCommand
from md_commands.step_start_command import StepStartCommand

def create_command(command_name: str, args: list[str]) -> Command:
    match command_name:
        case "atom_data_column":
            return AtomDataColumnCommand(command_name, args)
        case "atom_mass":
            return AtomMassCommand(command_name, args)
        case "cartesian_density_profile":
            return CartesianDensityProfileCommand(command_name, args)
        case "center_of_mass":
            return CenterOfMassCommand(command_name, args)
        case "data_path":
            return DataPathCommand(command_name, args)
        case "data_type":
            return DataTypeCommand(command_name, args)
        case "filter":
            return FilterCommand(command_name, args)
        case "first_neighbor_histogram":
            return FirstNeighborHistogramCommand(command_name, args)
        case "next_file":
            return NextFileCommand(command_name, args)
        case "radial_density_profile":
            return RadialDensityProfileCommand(command_name, args)
        case "read_file":
            return ReadFileCommand(command_name, args)
        case "step_end":
            return StepEndCommand(command_name, args)
        case "step_start":
            return StepStartCommand(command_name, args)
        case _:
            raise Exception(f"Unsupported command: {command_name}")