import datetime

from md_analyses.sanity_checks import atoms_within_box, total_atom_count, density_profile_atom_count
from md_dataclasses.atom import Atom
from md_dataclasses.box import Box
from md_dataclasses.density_profile import DensityProfile
from md_dataclasses.header import Header
from md_dataclasses.vector3d import Vector3D
from md_readers.config_reader import ConfigReader

def print_title(config: ConfigReader) -> str:
    text = f"ANALYSIS OF FILE(S) LOCATED AT: {config.data_path} (steps {config.step_start} through {config.step_end})"
    text += f"\nCompleted: {datetime.datetime.now()}"
    return text

def print_header(header: Header) -> str:
    return f"\n\nHeader data:\n{str(header)}"

def print_atom_extremes(atom_extremes: Box) -> str:
    return f"\n\nMost extreme atom coordinates:\n{atom_extremes}"

def print_sanity_checks(header: Header, atom_extremes: Box, atoms: list[Atom], density_profiles: dict[str, DensityProfile]) -> str:
    text = f"\n\nSanity checks:"
    text += f"\n{atoms_within_box(header.box, atom_extremes)}"
    text += f"\n{total_atom_count(header, len(atoms))}"

    for axis in ["x", "y", "z"]:
        # f-strings don't like square brackets
        profile = density_profiles[axis]
        text += f"\n{density_profile_atom_count(header, profile, axis)}"

    return text

def print_salt_concentration(salt_concentration: float) -> str:
    return f"\n\nSalt concentration:\n{salt_concentration * 100 :0.3f}%"

def print_vapor_count(vapor_count: float) -> str:
    return f"\n\nVapor count:\n{vapor_count}"

def print_droplet_center(droplet_com: Vector3D) -> str:
    return f"\n\nDroplet center of mass:\n{droplet_com}"

def print_files_used(data_files: list[str]) -> str:
    text = f"\n\nSpecific data files used:"
    for data_file in data_files:
        text += f"\n{data_file}"
    return text

def print_density_profile(profile: DensityProfile) -> str:
    text = profile.description
    for key, val in profile.data.items(): text += f"\n{key} {val}"
    return text