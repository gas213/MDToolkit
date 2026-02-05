from md_filters.filter_interface import Filter

class AtomTypeFilter(Filter):
    _atom_types: set[int]

    def __init__(self, atom_types: set[int]):
        self._atom_types = atom_types

    def apply(self, atoms):
        return [atom for atom in atoms if atom.type in self._atom_types]