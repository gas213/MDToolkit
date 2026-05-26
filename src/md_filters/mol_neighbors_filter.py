from md_domain.atom import Atom
from md_filters.filter_interface import Filter

class MoleculeNeighborsFilter(Filter):
    def __init__(self, filter_source_atoms: Filter, filter_potential_neighbor_atoms: Filter):
        self._filter_source_atoms = filter_source_atoms
        self._filter_potential_neighbor_atoms = filter_potential_neighbor_atoms

    def apply(self, atoms: list[Atom]) -> list[Atom]:
        atoms_filtered: list[Atom] = []
        atoms_source_mol_ids = set([atom.mol for atom in self._filter_source_atoms.apply(atoms)])
        atoms_potential_neighbors = self._filter_potential_neighbor_atoms.apply(atoms)
        for atom_potential_neighbor in atoms_potential_neighbors:
            if atom_potential_neighbor.mol in atoms_source_mol_ids:
                atoms_filtered.append(atom_potential_neighbor)
        return atoms_filtered