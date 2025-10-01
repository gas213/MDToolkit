import numpy as np
from numpy import ndarray

from md_dataclasses.atom import Atom

def build_profiles_cartesian(atoms: list[Atom], config: ConfigReader, header: Header, description: str) -> dict[str, DensityProfile]:
    x = build_profile([atom.pos.x for atom in atoms], build_bins_cartesian(header.box.lo.x, header.box.hi.x, config.cartesian_profile_step_xyz))
    y = build_profile([atom.pos.y for atom in atoms], build_bins_cartesian(header.box.lo.y, header.box.hi.y, config.cartesian_profile_step_xyz))
    z = build_profile([atom.pos.z for atom in atoms], build_bins_cartesian(header.box.lo.z, header.box.hi.z, config.cartesian_profile_step_xyz))

    return {
        "x": DensityProfile(x, f"Profile of {description} atom count in x:"),
        "y": DensityProfile(y, f"Profile of {description} atom count in y:"),
        "z": DensityProfile(z, f"Profile of {description} atom count in z:"),
    }

def build_profile(data: list[float], bins: ndarray) -> dict[str, float]:
    hist, _ = np.histogram(data, bins)
    
    labels = [f"[{bins[i]}, {bins[i + 1]})" for i in range(len(bins) - 1)]
    labels[-1] = labels[-1][:-1] + "]"  # The end of the last bin is inclusive

    return {k: v for k, v in zip(labels, hist)}

def build_bins_cartesian(start: float, stop: float, step: float) -> ndarray[float]:
    bins = np.arange(start, stop, step)
    if stop > bins[-1]: bins = np.append(bins, stop) # Append one last bin to cover the remainder (may be smaller than the other bins)
    return bins