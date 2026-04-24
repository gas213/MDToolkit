import numpy as np
from numpy import ndarray

from md_domain.atom import Atom
from md_enums.cartesian_axis import CartesianAxis

# ASSUMPTIONS:
# - Atom data is in LAMMPS 'real' units (atomic mass, Angstrom distances)
# - Normalization argument value is in g/cm^3
# - Cross section area is the box area perpendicular to the chosen axis, in A^2
UNIT_CONVERSION: float = 1.66054 # Conversion factor from amu/A^3 to g/cm^3

def build_cartesian_density_profile(atoms: list[Atom], axis: CartesianAxis, bin_start: float, bin_stop: float, bin_step: float, atom_masses: dict[int, float], normalization_density: float, cross_section_area: float) -> dict[float, float]:
    atoms_coord: list[float] = [getattr(atom.pos, axis.value) for atom in atoms]
    bins = build_bins(bin_start, bin_stop, bin_step)
    bin_volumes = cross_section_area * np.diff(bins)
    weights: list[float] = [atom_masses[atom.type] for atom in atoms]
    hist, _ = np.histogram(atoms_coord, bins, weights=weights)

    factor: float = UNIT_CONVERSION / normalization_density
    results: dict[float, float] = {}
    for i in range(len(bins) - 1):
        density = hist[i] / bin_volumes[i] * factor
        results[bins[i]] = density

    return results

def build_bins(start: float, stop: float, step: float) -> ndarray:
    bins = np.arange(start, stop, step)
    if stop > bins[-1]: bins = np.append(bins, stop) # Append one last bin to cover the remainder (may be smaller than the other bins)
    return bins
