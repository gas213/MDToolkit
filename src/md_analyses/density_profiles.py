import math
import numpy as np
from numpy import ndarray

from constants import four_thirds_pi
from md_dataclasses.atom import Atom
from md_dataclasses.density_profile import DensityProfile
from md_dataclasses.header import Header
from md_dataclasses.vector3d import Vector3D
from md_readers.config_reader import ConfigReader

def build_profiles_cartesian(atoms: list[Atom], config: ConfigReader, header: Header, description: str) -> dict[str, DensityProfile]:
    x = build_profile([atom.pos.x for atom in atoms], build_bins_cartesian(header.box.lo.x, header.box.hi.x, config.cartesian_profile_step_xyz))
    y = build_profile([atom.pos.y for atom in atoms], build_bins_cartesian(header.box.lo.y, header.box.hi.y, config.cartesian_profile_step_xyz))
    z = build_profile([atom.pos.z for atom in atoms], build_bins_cartesian(header.box.lo.z, header.box.hi.z, config.cartesian_profile_step_xyz))

    return {
        "x": DensityProfile(x, f"Profile of {description} atom count in x:"),
        "y": DensityProfile(y, f"Profile of {description} atom count in y:"),
        "z": DensityProfile(z, f"Profile of {description} atom count in z:"),
    }

def build_profiles_spherical(atoms: list[Atom], config: ConfigReader, droplet_com: Vector3D, description: str) -> dict[str, DensityProfile]:
    r_bins = build_bins_spherical(config.spherical_profile_start_r, config.approx_sphere["R"], config.spherical_profile_step_r)
    r_count = build_profile([math.sqrt((atom.pos.x - droplet_com.x)**2 + (atom.pos.y - droplet_com.y)**2 + (atom.pos.z - droplet_com.z)**2) for atom in atoms], r_bins)

    r_bin_volumes = [four_thirds_pi * (r_bins[i + 1]**3 - r_bins[i]**3) for i in range(len(r_bins) - 1)]
    r_density = {k: v for k, v in zip(r_count.keys(), [list(r_count.values())[i] / r_bin_volumes[i] for i in range(len(r_count))])}

    r_count_total = sum(r_count.values())
    v_characteristic = four_thirds_pi * float(config.approx_sphere["R"])**3
    norm_factor = 1.0 if r_count_total == 0 else v_characteristic / r_count_total

    r_density_norm = {k: v for k, v in zip(r_count.keys(), np.array(list(r_density.values())) * norm_factor)}

    return {
        "r_count": DensityProfile(r_count, f"Profile of {description} atom count vs truncated radius, based on droplet center of mass:"),
        "r_density": DensityProfile(r_density, f"Profile of {description} density (atoms/angstrom**3) vs truncated radius, based on droplet center of mass:"),
        "r_density_norm": DensityProfile(r_density_norm, f"Profile of {description} normalized density vs truncated radius, based on droplet center of mass:"),
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

def build_bins_spherical(start: float, stop: float, step: float) -> ndarray[float]:
    bins = np.append([0.0], np.arange(start, stop, step)) # First bin is the spherical "core"
    if stop > bins[-1]: bins = np.append(bins, stop) # Append one last bin to cover the remainder (may be smaller than the other bins)
    return bins