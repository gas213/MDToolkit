from md_filters.filter_interface import Filter

class CartesianFilter(Filter):
    _x_min: float
    _x_max: float
    _y_min: float
    _y_max: float
    _z_min: float
    _z_max: float

    def __init__(self, x_min: float, x_max: float, y_min: float, y_max: float, z_min: float, z_max: float):
        self._x_min = x_min
        self._x_max = x_max
        self._y_min = y_min
        self._y_max = y_max
        self._z_min = z_min
        self._z_max = z_max

    def apply(self, atoms):
        atoms_filtered = atoms[:]
        if self._x_min is not None and self._x_max is not None:
            atoms_filtered = [atom for atom in atoms_filtered if self._x_min <= atom.pos.x <= self._x_max]
        elif self._x_min is None:
            atoms_filtered = [atom for atom in atoms_filtered if atom.pos.x <= self._x_max]
        elif self._x_max is None:
            atoms_filtered = [atom for atom in atoms_filtered if atom.pos.x >= self._x_min]
        if self._y_min is not None and self._y_max is not None:
            atoms_filtered = [atom for atom in atoms_filtered if self._y_min <= atom.pos.y <= self._y_max]
        elif self._y_min is None:
            atoms_filtered = [atom for atom in atoms_filtered if atom.pos.y <= self._y_max]
        elif self._y_max is None:
            atoms_filtered = [atom for atom in atoms_filtered if atom.pos.y >= self._y_min]
        if self._z_min is not None and self._z_max is not None:
            atoms_filtered = [atom for atom in atoms_filtered if self._z_min <= atom.pos.z <= self._z_max]
        elif self._z_min is None:
            atoms_filtered = [atom for atom in atoms_filtered if atom.pos.z <= self._z_max]
        elif self._z_max is None:
            atoms_filtered = [atom for atom in atoms_filtered if atom.pos.z >= self._z_min]
        return atoms_filtered