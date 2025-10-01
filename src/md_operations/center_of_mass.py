from md_dataclasses.atom import Atom
from md_dataclasses.vector3d import Vector3D

def calc_center_of_mass(atoms: list[Atom], atom_masses: dict[int, float]) -> Vector3D:
    sum_by_type_x: dict[int, float] = {}
    sum_by_type_y: dict[int, float] = {}
    sum_by_type_z: dict[int, float] = {}
    for atom_type in atom_masses.keys():
        sum_by_type_x[atom_type] = 0.0
        sum_by_type_y[atom_type] = 0.0
        sum_by_type_z[atom_type] = 0.0

    sum_m = 0.0
    for atom in atoms:
        sum_by_type_x[atom.type] += atom.pos.x
        sum_by_type_y[atom.type] += atom.pos.y
        sum_by_type_z[atom.type] += atom.pos.z
        sum_m += atom_masses[atom.type]

    sum_mx: float = 0.0
    sum_my: float = 0.0
    sum_mz: float = 0.0
    for atom_type, atom_mass in atom_masses.items():
        sum_mx += atom_mass * sum_by_type_x[atom_type]
        sum_my += atom_mass * sum_by_type_y[atom_type]
        sum_mz += atom_mass * sum_by_type_z[atom_type]
    
    return Vector3D(0.0, 0.0, 0.0) if sum_m == 0.0 else Vector3D(sum_mx / sum_m, sum_my / sum_m, sum_mz / sum_m)