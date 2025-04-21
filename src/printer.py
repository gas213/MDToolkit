import datetime

from md_analyses.sanity_checks import atoms_within_box, total_atom_count, density_profile_atom_count
from md_dataclasses.atom import Atom
from md_dataclasses.box import Box
from md_dataclasses.density_profile import DensityProfile
from md_dataclasses.header import Header

def print_title(data_path: str) -> str:
    return f"ANALYSIS OF FILE LOCATED AT: {data_path}\nPerformed: {datetime.datetime.now()}"

def print_header(header: Header) -> str:
    return f"\n\nHeader data:\n{str(header)}"

def print_atom_extremes(atom_extremes: Box) -> str:
    return f"\n\nMost extreme atom coordinates:\n{atom_extremes}"

def print_sanity_checks(header: Header, atom_extremes: Box, atoms: list[Atom], density_profiles: dict[str, DensityProfile]) -> str:
    text = f"\n\nSanity checks:"
    text += f"\n{atoms_within_box(header.box, atom_extremes)}"
    text += f"\n{total_atom_count(header, len(atoms))}"

    # f-strings don't like square brackets
    dens_x = density_profiles["x"]
    dens_y = density_profiles["y"]
    dens_z = density_profiles["z"]
    text += f"\n{density_profile_atom_count(header, dens_x, dens_y, dens_z)}"
    return text

def print_salt_concentration(salt_concentration: float) -> str:
    return f"\n\nSalt concentration:\n{salt_concentration * 100 :0.3f}%"

def print_vapor_count(vapor_count: int) -> str:
    return f"\n\nVapor count:\n{vapor_count}"

def print_droplet_center(droplet_center: Box) -> str:
    return f"\n\nDroplet center of mass:\n{droplet_center}"

def print_density_profile(profile: DensityProfile) -> str:
    text = profile.description
    for key, val in profile.data.items(): text += f"\n{key} {val}"
    return text