import numpy as np
from numpy import ndarray

from md_dataclasses.atom import Atom
from md_dataclasses.vector3d import Vector3D

def build_radial_density_profile(atoms: list[Atom], origin: Vector3D, bin_start: float, bin_stop: float, bin_step: float) -> dict[float, float]:
    atoms_r2: list[float] = [(atom.pos.x - origin.x)**2 + (atom.pos.y - origin.y)**2 + (atom.pos.z - origin.z)**2 for atom in atoms]
    bins_r = build_bins(bin_start, bin_stop, bin_step)
    bins_r2 = np.array([bin_r**2 for bin_r in bins_r])
    bin_volumes = [4.0 / 3.0 * np.pi * (bins_r[i + 1]**3 - bins_r[i]**3) for i in range(len(bins_r) - 1)]
    hist, _ = np.histogram(atoms_r2, bins_r2)
    
    results: dict[float, float] = {}
    for i in range(len(bins_r) - 1):
        density = hist[i] / bin_volumes[i]
        results[bins_r[i]] = density

    return results

def build_bins(start: float, stop: float, step: float) -> ndarray[float]:
    bins = np.append([0.0], np.arange(start, stop, step)) # First bin is the central "core"
    if stop > bins[-1]: bins = np.append(bins, stop) # Append one last bin to cover the remainder (may be smaller than the other bins)
    return bins