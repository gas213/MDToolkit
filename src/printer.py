import datetime

from sanity_checks import atoms_within_box, total_atom_count, density_profile_atom_count

def print_title(data_path):
    text = "ANALYSIS OF DATA FILE LOCATED AT: " + data_path
    text += "\nPerformed: " + str(datetime.datetime.now())
    return text

def print_header(header):
    text = "\n\nHeader data:"
    for name, val in header._asdict().items(): text += "\n" + name + ": " + str(val)
    return text

def print_atom_extremes(atom_extremes):
    text = "\n\nMost extreme atom coordinates:"
    text += "\n" + str(atom_extremes)
    return text

def print_sanity_checks(header, atom_extremes, atoms, atom_count_profiles):
    text = "\n\nSanity checks:"
    text += "\n" + atoms_within_box(header.box, atom_extremes)
    text += "\n" + total_atom_count(header, len(atoms))
    text += "\n" + density_profile_atom_count(header, atom_count_profiles)
    return text

def print_vapor_count(vapor_count):
    text = "\n\nVapor count: "
    text += "\n" + str(vapor_count)
    return text

def print_droplet_center(droplet_center):
    text = "\n\nDroplet center of mass: "
    text += "\n" + str(droplet_center)
    return text

def print_density_profiles(atom_count_profiles, name):
    text = "\n\nProfile of " + name + " density by truncated radius, based on droplet center of mass:"
    for key, val in atom_count_profiles.r_density.items(): text += "\n" + str(key) + " " + str(val)
    text += "\n\nProfile of " + name + " count by truncated radius, based on droplet center of mass:"
    for key, val in atom_count_profiles.r_count.items(): text += "\n" + str(key) + " " + str(val)
    text += "\n\nProfile of " + name + " count by truncated x coordinate:"
    for key, val in atom_count_profiles.x.items(): text += "\n" + str(key) + " " + str(val)
    text += "\n\nProfile of " + name + " count by truncated y coordinate:"
    for key, val in atom_count_profiles.y.items(): text += "\n" + str(key) + " " + str(val)
    text += "\n\nProfile of " + name + " count by truncated z coordinate:"
    for key, val in atom_count_profiles.z.items(): text += "\n" + str(key) + " " + str(val)
    return text