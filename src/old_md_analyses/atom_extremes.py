from md_domain.atom import Atom
from md_domain.box import Box
from md_domain.vector3d import Vector3D

def find_atom_extremes(atoms: list[Atom]) -> Box:
    xlo = atoms[0].pos.x
    xhi = atoms[0].pos.x
    ylo = atoms[0].pos.y
    yhi = atoms[0].pos.y
    zlo = atoms[0].pos.z
    zhi = atoms[0].pos.z
    for atom in atoms:
        if atom.pos.x < xlo: xlo = atom.pos.x
        if atom.pos.x > xhi: xhi = atom.pos.x
        if atom.pos.y < ylo: ylo = atom.pos.y
        if atom.pos.y > yhi: yhi = atom.pos.y
        if atom.pos.z < zlo: zlo = atom.pos.z
        if atom.pos.z > zhi: zhi = atom.pos.z

    return Box(Vector3D(xlo, ylo, zlo), Vector3D(xhi, yhi, zhi))