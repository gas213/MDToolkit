from md_dataclasses.box import Box
from md_dataclasses.density_profile import DensityProfile
from md_dataclasses.header import Header

def atoms_within_box(box: Box, atom_extremes: Box) -> str:
    result = (box.lo.x <= atom_extremes.lo.x and box.hi.x >= atom_extremes.hi.x and
              box.lo.y <= atom_extremes.lo.y and box.hi.y >= atom_extremes.hi.y and
              box.lo.z <= atom_extremes.lo.z and box.hi.z >= atom_extremes.hi.z)
    return f"All atoms positioned with box: {result}"

def total_atom_count(header: Header, len_atoms: int) -> str:
    result = (header.atom_count == len_atoms)
    return f"Atom count in header matches number of atom records: {result}"

def density_profile_atom_count(header: Header, x_profile: DensityProfile, y_profile: DensityProfile, z_profile: DensityProfile) -> str:
    result = (header.atom_count == sum(x_profile.data.values()) and
              header.atom_count == sum(y_profile.data.values()) and
              header.atom_count == sum(z_profile.data.values()))
    return f"Box-wise density profiles each include every atom: {result}"