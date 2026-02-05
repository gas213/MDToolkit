from md_filters.filter_interface import Filter

class AndFilter(Filter):
    _filters: list[Filter]

    def __init__(self, filters: list[Filter]):
        self._filters = filters

    def apply(self, atoms):
        atoms_filtered = atoms[:]
        for filter in self._filters:
            atoms_filtered = filter.apply(atoms_filtered)
        return atoms_filtered