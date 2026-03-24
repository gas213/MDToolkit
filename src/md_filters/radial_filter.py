from md_dataclasses.atom import Atom
from md_filters.filter_interface import Filter

class RadialFilter(Filter):
    def __init__(self, x: float, y: float, z: float, r_min: float | None, r_max: float | None):
        self._x = x
        self._y = y
        self._z = z
        self._r_min = r_min
        self._r_max = r_max

    def apply(self, atoms: list[Atom]) -> list[Atom]:
        atoms_filtered = atoms[:]
        if self._r_min is None and self._r_max is not None:
            r2_max: float = self._r_max**2
            atoms_filtered = [atom for atom in atoms if (atom.pos.x - self._x)**2 + (atom.pos.y - self._y)**2 + (atom.pos.z - self._z)**2 <= r2_max]
        elif self._r_min is not None and self._r_max is None:
            r2_min: float = self._r_min**2
            atoms_filtered = [atom for atom in atoms if (atom.pos.x - self._x)**2 + (atom.pos.y - self._y)**2 + (atom.pos.z - self._z)**2 >= r2_min]
        elif self._r_min is not None and self._r_max is not None:
            # Shell region
            r2_min: float = self._r_min**2
            r2_max: float = self._r_max**2
            atoms_filtered = [atom for atom in atoms if r2_min <= (atom.pos.x - self._x)**2 + (atom.pos.y - self._y)**2 + (atom.pos.z - self._z)**2 <= r2_max]
        return atoms_filtered