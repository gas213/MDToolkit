from enum import Enum
from typing import Type, TypeVar

from md_commands.atom_data_column_command import AtomDataColumnCommand
from md_commands.atom_mass_command import AtomMassCommand
from md_commands.center_of_mass_command import CenterOfMassCommand
from md_commands.command_helpers import parse_float, parse_int
from md_commands.command_interface import Command
from md_commands.data_path_command import DataPathCommand
from md_commands.data_type_command import DataTypeCommand
from md_commands.filter_command import FilterCommand
from md_commands.next_file_command import NextFileCommand
from md_commands.radial_density_profile_command import RadialDensityProfileCommand
from md_commands.read_atoms_command import ReadAtomsCommand
from md_commands.read_header_command import ReadHeaderCommand
from md_commands.salt_histograms_command import SaltHistogramsCommand
from md_commands.step_end_command import StepEndCommand
from md_commands.step_start_command import StepStartCommand
from md_enums.aggregation_type import AggregationType
from md_enums.atom_data_column_type import AtomDataColumnType
from md_enums.data_file_type import DataFileType
from md_enums.filter_type import FilterType

T = TypeVar("T", bound=Enum)

def create_command(command_name: str, args: list[str]) -> Command:
    match command_name:
        case "atom_data_column":
            return create_atom_data_column_command(command_name, args)
        case "atom_mass":
            return create_atom_mass_command(command_name, args)
        case "center_of_mass":
            return create_center_of_mass_command(command_name, args)
        case "data_path":
            return create_data_path_command(command_name, args)
        case "data_type":
            return create_data_type_command(command_name, args)
        case "filter":
            return create_filter_command(command_name, args)
        case "next_file":
            return create_next_file_command(command_name, args)
        case "radial_density_profile":
            return create_radial_density_profile_command(command_name, args)
        case "read_atoms":
            return create_read_atoms_command(command_name, args)
        case "read_header":
            return create_read_header_command(command_name, args)
        case "salt_histograms":
            return create_salt_histograms_command(command_name, args)
        case "step_end":
            return create_step_end_command(command_name, args)
        case "step_start":
            return create_step_start_command(command_name, args)
        case _:
            raise Exception(f"Unsupported command: {command_name}")

def check_for_exact_arg_count(command_name: str, args: list[str], expected_arg_count: int):
    if len(args) != expected_arg_count:
        raise Exception(f"{command_name} command does not have the right number of args (expected {expected_arg_count}, got {len(args)})")
    
def check_for_min_arg_count(command_name: str, args: list[str], min_arg_count: int):
    if len(args) < min_arg_count:
        raise Exception(f"{command_name} command does not have enough args (expected at least {min_arg_count}, got {len(args)})")

def check_categorical_arg(command_name: str, arg_value: str, enum_class: Type[T]) -> T:
    if not any(arg_value == item.value for item in enum_class):
        raise Exception(f"Unsupported {command_name} argument value specified in configuration: '{arg_value}' (supported values are {[item.value for item in enum_class]})")
    return enum_class(arg_value)

def create_atom_data_column_command(command_name: str, args: list[str]) -> AtomDataColumnCommand:
    check_for_exact_arg_count(command_name, args, 2)
    column_type = check_categorical_arg(command_name, args[0].lower(), AtomDataColumnType)
    return AtomDataColumnCommand(column_type, parse_int(args[1]))

def create_atom_mass_command(command_name: str, args: list[str]) -> AtomMassCommand:
    check_for_exact_arg_count(command_name, args, 2)
    return AtomMassCommand(parse_int(args[0]), parse_float(args[1]))

def create_center_of_mass_command(command_name: str, args: list[str]) -> CenterOfMassCommand:
    check_for_exact_arg_count(command_name, args, 1)
    aggregation_type = check_categorical_arg(command_name, args[0].lower(), AggregationType)
    return CenterOfMassCommand(aggregation_type)

def create_data_path_command(command_name: str, args: list[str]) -> DataPathCommand:
    check_for_exact_arg_count(command_name, args, 1)
    return DataPathCommand(args[0])

def create_data_type_command(command_name: str, args: list[str]) -> DataTypeCommand:
    check_for_exact_arg_count(command_name, args, 1)
    data_file_type = check_categorical_arg(command_name, args[0].lower(), DataFileType)
    return DataTypeCommand(data_file_type)

def create_filter_command(command_name: str, args: list[str]) -> FilterCommand:
    check_for_min_arg_count(command_name, args, 2)
    if args[0].lower() == "all":
        raise Exception("Filter name cannot be 'all' because it is a reserved keyword")
    filter_type = check_categorical_arg(command_name, args[1].lower(), FilterType)
    filter_params = args[2:] if len(args) > 2 else []
    return FilterCommand(args[0], filter_type, filter_params)

def create_next_file_command(command_name: str, args: list[str]) -> NextFileCommand:
    check_for_exact_arg_count(command_name, args, 0)
    return NextFileCommand()

def create_radial_density_profile_command(command_name: str, args: list[str]) -> RadialDensityProfileCommand:
    check_for_exact_arg_count(command_name, args, 4)
    aggregation_type = check_categorical_arg(command_name, args[0].lower(), AggregationType)
    return RadialDensityProfileCommand(aggregation_type, parse_float(args[1]), parse_float(args[2]), parse_float(args[3]))

def create_read_atoms_command(command_name: str, args: list[str]) -> ReadAtomsCommand:
    check_for_exact_arg_count(command_name, args, 0)
    return ReadAtomsCommand()

def create_read_header_command(command_name: str, args: list[str]) -> ReadHeaderCommand:
    check_for_exact_arg_count(command_name, args, 0)
    return ReadHeaderCommand()

def create_salt_histograms_command(command_name: str, args: list[str]) -> SaltHistogramsCommand:
    check_for_exact_arg_count(command_name, args, 2)
    aggregation_type = check_categorical_arg(command_name, args[1].lower(), AggregationType)
    return SaltHistogramsCommand(args[0], aggregation_type)

def create_step_end_command(command_name: str, args: list[str]) -> StepEndCommand:
    check_for_exact_arg_count(command_name, args, 1)
    return StepEndCommand(parse_int(args[0]))

def create_step_start_command(command_name: str, args: list[str]) -> StepStartCommand:
    check_for_exact_arg_count(command_name, args, 1)
    return StepStartCommand(parse_int(args[0]))