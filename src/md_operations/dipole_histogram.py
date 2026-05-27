import numpy as np

from md_domain.atom import Atom
from md_domain.vector3d import Vector3D

def build_dipole_histogram_data(atoms_o: list[Atom], atoms_h: list[Atom], origin: Vector3D, n_bins: int) -> dict[float, float]:
    data: dict[float, float] = {}
    cosines: list[float] = []
    dict_mol_hydrogens: dict[int, list[Atom]] = {}
    for atom_h in atoms_h:
        if atom_h.mol not in dict_mol_hydrogens:
            dict_mol_hydrogens[atom_h.mol] = []
        dict_mol_hydrogens[atom_h.mol].append(atom_h)

    for atom_o in atoms_o:
        neighbors_h = dict_mol_hydrogens.get(atom_o.mol, [])
        if len(neighbors_h) != 2:
            raise Exception(f"Error in dipole_histogram analysis: expected to find 2 hydrogens with molecule ID {atom_o.mol} (oxygen atom ID {atom_o.id}), but instead found {len(neighbors_h)}.")
        vec_origin_to_o: Vector3D = atom_o.pos - origin
        h_midpoint: Vector3D = (neighbors_h[0].pos + neighbors_h[1].pos) * 0.5
        vec_dipole: Vector3D = atom_o.pos - h_midpoint
        cosines.append(np.dot(vec_origin_to_o.to_array(), vec_dipole.to_array()) / (np.linalg.norm(vec_origin_to_o.to_array()) * np.linalg.norm(vec_dipole.to_array())))

    bins = np.linspace(-1.0, 1.0, n_bins + 1)
    hist, _ = np.histogram(cosines, bins=bins)
    norm_factor: float = 1.0 / len(cosines)
    for bin_start, value in zip(bins[:-1], hist):
        data[bin_start] = value * norm_factor
        
    return data