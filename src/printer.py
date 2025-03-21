import datetime

from md_analyses.sanity_checks import atoms_within_box, total_atom_count, density_profile_atom_count

def print_title(data_path):
    return f"ANALYSIS OF DATA FILE LOCATED AT: {data_path}\nPerformed: {datetime.datetime.now()}"

def print_header(header):
    return f"\n\nHeader data:\n{str(header)}"

def print_atom_extremes(atom_extremes):
    return f"\n\nMost extreme atom coordinates:\n{atom_extremes}"

def print_sanity_checks(header, atom_extremes, atoms, atom_count_profiles):
    text = f"\n\nSanity checks:"
    text += f"\n{atoms_within_box(header.box, atom_extremes)}"
    text += f"\n{total_atom_count(header, len(atoms))}"
    text += f"\n{density_profile_atom_count(header, atom_count_profiles)}"
    return text

def print_salt_concentration(salt_concentration):
    return f"\n\nSalt concentration:\n{salt_concentration * 100 :0.3f}%"

def print_vapor_count(vapor_count):
    return f"\n\nVapor count:\n{vapor_count}"

def print_droplet_center(droplet_center):
    return f"\n\nDroplet center of mass:\n{droplet_center}"

def print_density_profiles(atom_count_profiles, name):
    text = f"\n\nProfile of {name} normalized density vs truncated radius, based on droplet center of mass:"
    for key, val in atom_count_profiles.r_density_norm.items(): text += f"\n{key} {val}"
    text += f"\n\nProfile of {name} density (atoms/angstrom**3) vs truncated radius, based on droplet center of mass:"
    for key, val in atom_count_profiles.r_density.items(): text += f"\n{key} {val}"
    text += f"\n\nProfile of {name} count vs truncated radius, based on droplet center of mass:"
    for key, val in atom_count_profiles.r_count.items(): text += f"\n{key} {val}"
    text += f"\n\nProfile of {name} count vs truncated x coordinate:"
    for key, val in atom_count_profiles.x.items(): text += f"\n{key} {val}"
    text += f"\n\nProfile of {name} count vs truncated y coordinate:"
    for key, val in atom_count_profiles.y.items(): text += f"\n{key} {val}"
    text += f"\n\nProfile of {name} count vs truncated z coordinate:"
    for key, val in atom_count_profiles.z.items(): text += f"\n{key} {val}"
    return text