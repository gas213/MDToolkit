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