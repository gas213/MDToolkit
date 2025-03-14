def atoms_within_box(box, atom_extremes):
    result = (box.xlo <= atom_extremes.xlo and box.xhi >= atom_extremes.xhi and
              box.ylo <= atom_extremes.ylo and box.yhi >= atom_extremes.yhi and
              box.zlo <= atom_extremes.zlo and box.zhi >= atom_extremes.zhi)
    return "All atoms positioned with box: " + str(result)

def total_atom_count(header, len_atoms):
    result = (header.atom_count == len_atoms)
    return "Atom count in header matches number of atom records: " + str(result)

def density_profile_atom_count(header, profiles):
    result = (header.atom_count == sum(profiles.x.values()) and
              header.atom_count == sum(profiles.y.values()) and
              header.atom_count == sum(profiles.z.values()))
    return "Box-wise density profiles each include every atom: " + str(result)