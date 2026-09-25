from md_domain.atom import Atom
from md_filters.filter_interface import Filter

class CylindricalZFilter(Filter):
    def __init__(self, x: float, y: float, z_min: float | None, z_max: float | None, r_min: float | None, r_max: float | None):
        self._x = x
        self._y = y
        self._z_min = z_min
        self._z_max = z_max
        self._r_min = r_min
        self._r_max = r_max

    def apply(self, atoms: list[Atom]) -> list[Atom]:
        atoms_filtered = atoms[:]
        if self._r_min is None and self._r_max is not None:
            r2_max: float = self._r_max**2
            atoms_filtered = [atom for atom in atoms if (atom.pos.x - self._x)**2 + (atom.pos.y - self._y)**2 <= r2_max and (self._z_min is None or atom.pos.z >= self._z_min) and (self._z_max is None or atom.pos.z <= self._z_max)]
        elif self._r_min is not None and self._r_max is None:
            r2_min: float = self._r_min**2
            atoms_filtered = [atom for atom in atoms if (atom.pos.x - self._x)**2 + (atom.pos.y - self._y)**2 >= r2_min and (self._z_min is None or atom.pos.z >= self._z_min) and (self._z_max is None or atom.pos.z <= self._z_max)]
        elif self._r_min is not None and self._r_max is not None:
            # Shell region
            r2_min: float = self._r_min**2
            r2_max: float = self._r_max**2
            atoms_filtered = [atom for atom in atoms if r2_min <= (atom.pos.x - self._x)**2 + (atom.pos.y - self._y)**2 <= r2_max and (self._z_min is None or atom.pos.z >= self._z_min) and (self._z_max is None or atom.pos.z <= self._z_max)]
        return atoms_filtered