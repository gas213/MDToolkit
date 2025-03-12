from named_tuples import Box

def find_atom_extremes(atoms):
    xlo = atoms[0].x
    xhi = atoms[0].x
    ylo = atoms[0].y
    yhi = atoms[0].y
    zlo = atoms[0].z
    zhi = atoms[0].z
    for atom in atoms:
        if atom.x < xlo: xlo = atom.x
        if atom.x > xhi: xhi = atom.x
        if atom.y < ylo: ylo = atom.y
        if atom.y > yhi: yhi = atom.y
        if atom.z < zlo: zlo = atom.z
        if atom.z > zhi: zhi = atom.z

    return Box(xlo, xhi, ylo, yhi, zlo, zhi)

def atoms_within_box(box, atom_extremes):
    result = (box.xlo <= atom_extremes.xlo and box.xhi >= atom_extremes.xhi and
              box.ylo <= atom_extremes.ylo and box.yhi >= atom_extremes.yhi and
              box.zlo <= atom_extremes.zlo and box.zhi >= atom_extremes.zhi)
    return "All atoms positioned with box: " + str(result)

def total_atom_count(header, len_atoms):
    result = (header.atom_count == len_atoms)
    return "Atom count in header matches number of atom records: " + str(result)

def density_profile_atom_count(header, density_profiles):
    result = (header.atom_count == sum(density_profiles.x.values()) and
              header.atom_count == sum(density_profiles.y.values()) and
              header.atom_count == sum(density_profiles.z.values()))
    return "Density profiles each include every atom: " + str(result)