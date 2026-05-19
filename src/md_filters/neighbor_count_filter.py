from md_domain.atom import Atom
from md_filters.filter_interface import Filter

class NeighborCountFilter(Filter):
    def __init__(self, filter_central_atoms: Filter, filter_neighbor_atoms: Filter, neighbor_count_min: int | None, neighbor_count_max: int | None, r_cutoff: float):
        self._filter_central_atoms = filter_central_atoms
        self._filter_neighbor_atoms = filter_neighbor_atoms
        self._neighbor_count_min = neighbor_count_min
        self._neighbor_count_max = neighbor_count_max
        self._r_cutoff_sq = r_cutoff ** 2

    def apply(self, atoms: list[Atom]) -> list[Atom]:
        atoms_filtered: list[Atom] = []
        atoms_central = self._filter_central_atoms.apply(atoms)
        atoms_neighbor = self._filter_neighbor_atoms.apply(atoms)
        for atom_central in atoms_central:
            neighbor_count: int = sum(1 for atom_neighbor in atoms_neighbor if (atom_central.pos.x - atom_neighbor.pos.x)**2 + (atom_central.pos.y - atom_neighbor.pos.y)**2 + (atom_central.pos.z - atom_neighbor.pos.z)**2 <= self._r_cutoff_sq)
            if self._neighbor_count_min is not None and neighbor_count < self._neighbor_count_min:
                continue
            if self._neighbor_count_max is not None and neighbor_count > self._neighbor_count_max:
                continue
            atoms_filtered.append(atom_central)
        return atoms_filtered