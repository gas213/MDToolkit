from md_domain.atom import Atom
from md_filters.filter_interface import Filter

class UnionFilter(Filter):
    def __init__(self, filters: list[Filter]):
        self._filters = filters

    def apply(self, atoms: list[Atom]) -> list[Atom]:
        atoms_filtered_ids: set[int] = set()
        for filter in self._filters:
            for atom in filter.apply(atoms):
                atoms_filtered_ids.add(atom.id)
        atoms_filtered: list[Atom] = []
        for atom in atoms:
            if atom.id in atoms_filtered_ids:
                atoms_filtered.append(atom)
        return atoms_filtered