import math
import numpy as np

from constants import four_thirds_pi
from md_dataclasses.atom import Atom
from md_dataclasses.density_profile import DensityProfile
from md_dataclasses.header import Header
from md_dataclasses.vector3d import Vector3D
from md_readers.config_reader import ConfigReader

def build_histogram(start: float, end: float, interval: float, data: list[float]) -> dict[str, float]:
    bins = np.arange(start, end, interval)
    if end > bins[-1]: bins = np.append(bins, end) # Append one last bin to cover the remainder (will likely be smaller than the other bins)
    hist, _ = np.histogram(data, bins)
    
    labels = [f"[{bins[i]}, {bins[i + 1]})" for i in range(len(bins) - 1)]
    labels[-1] = labels[-1][:-1] + "]"  # The end of the last bin is inclusive

    return {k: v for k, v in zip(labels, hist)}
    
def build_density_profiles(config: ConfigReader, header: Header, atoms: list[Atom], droplet_com: Vector3D, description: str) -> dict[str, DensityProfile]:
    x = build_histogram(header.box.lo.x, header.box.hi.x, config.cartesian_profile_interval, [atom.pos.x for atom in atoms])
    y = build_histogram(header.box.lo.y, header.box.hi.y, config.cartesian_profile_interval, [atom.pos.y for atom in atoms])
    z = build_histogram(header.box.lo.z, header.box.hi.z, config.cartesian_profile_interval, [atom.pos.z for atom in atoms])
    
    x_c = droplet_com.x
    y_c = droplet_com.y
    z_c = droplet_com.z
    r_count = dict()
    r_density = dict()
    r_density_norm = dict()
    # TODO: fix range, shouldn't be casting to int
    for val in range(int(config.radial_profile_start_r), int(config.approx_sphere["R"])): r_count[val] = 0
    for val in range(int(config.radial_profile_start_r), int(config.approx_sphere["R"])): r_density[val] = 0
    for val in range(int(config.radial_profile_start_r), int(config.approx_sphere["R"])): r_density_norm[val] = 0

    for atom in atoms:
        r_atom = math.sqrt((atom.pos.x - x_c)**2 + (atom.pos.y - y_c)**2 + (atom.pos.z - z_c)**2)
        if int(r_atom) in r_count: r_count[int(r_atom)] += 1

    r_count_total = sum(r_count.values())
    v_total = four_thirds_pi * float(config.approx_sphere["R"])**3
    norm_factor = 1 if r_count_total == 0 else v_total / r_count_total

    v_inner = four_thirds_pi * config.radial_profile_start_r**3
    # TODO: fix range, shouldn't be casting to int
    for r_inner in range(int(config.radial_profile_start_r), int(config.approx_sphere["R"])):
        v_outer = four_thirds_pi * float(r_inner + 1)**3
        r_density[r_inner] = float(r_count[r_inner]) / (v_outer - v_inner)
        r_density_norm[r_inner] = r_density[r_inner] * norm_factor
        v_inner = v_outer

    return {
        "x": DensityProfile(x, f"Profile of {description} atom count in x:"),
        "y": DensityProfile(y, f"Profile of {description} atom count in y:"),
        "z": DensityProfile(z, f"Profile of {description} atom count in z:"),
        "r_count": DensityProfile(r_count, f"Profile of {description} atom count vs truncated radius, based on droplet center of mass:"),
        "r_density": DensityProfile(r_density, f"Profile of {description} density (atoms/angstrom**3) vs truncated radius, based on droplet center of mass:"),
        "r_density_norm": DensityProfile(r_density_norm, f"Profile of {description} normalized density vs truncated radius, based on droplet center of mass:"),
    }