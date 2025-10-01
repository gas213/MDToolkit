import math
import numpy as np
from numpy import ndarray

from old_constants import four_thirds_pi
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

def build_profiles_cylindrical(atoms: list[Atom], config: ConfigReader, header: Header, wetted_area: dict[str, float], description: str) -> dict[str, DensityProfile]:
    x_wet: float = wetted_area["x"]
    y_wet: float = wetted_area["y"]
    r_wet: float = wetted_area["r"] * 1.2 # TODO: constant value? Pull out into constants or config file? It is supposed to be a buffer to capture a little data outside the wetted area
    r2_wet: float = r_wet**2
    height_z: float = header.box.hi.z - header.box.lo.z
    
    # Filter atoms down to those that are actually within the full cylinder (rough filter first)
    atoms_cyl = [a for a in atoms if a.pos.x >= (x_wet - r_wet) and a.pos.x <= (x_wet + r_wet) and a.pos.y >= (y_wet - r_wet) and a.pos.y <= (y_wet + r_wet)]
    atoms_cyl = [a for a in atoms_cyl if (a.pos.x - x_wet)**2 + (a.pos.y - y_wet)**2 <= r2_wet]

    r_bins = build_bins_radial(config.cylindrical_profile_start_r, r_wet, config.cylindrical_profile_step_r)
    r_count = build_profile([math.sqrt((a.pos.x - x_wet)**2 + (a.pos.y - y_wet)**2) for a in atoms_cyl], r_bins)

    r_bin_volumes = [math.pi * (r_bins[i + 1]**2 - r_bins[i]**2) * height_z for i in range(len(r_bins) - 1)]
    r_density = {k: v for k, v in zip(r_count.keys(), [list(r_count.values())[i] / r_bin_volumes[i] for i in range(len(r_count))])}

    r_count_total = sum(r_count.values())
    v_characteristic = math.pi * r2_wet * height_z
    norm_factor = 1.0 if r_count_total == 0 else v_characteristic / r_count_total
    r_density_norm = {k: v for k, v in zip(r_count.keys(), np.array(list(r_density.values())) * norm_factor)}

    z_bins = build_bins_cartesian(header.box.lo.z, header.box.hi.z, config.cylindrical_profile_step_z)
    z_count = build_profile([atom.pos.z for atom in atoms_cyl], z_bins)

    z_bin_volumes = [math.pi * r2_wet * (z_bins[i + 1] - z_bins[i]) for i in range(len(z_bins) - 1)]
    z_density = {k: v for k, v in zip(z_count.keys(), [list(z_count.values())[i] / z_bin_volumes[i] for i in range(len(z_count))])}

    z_count_total = sum(z_count.values())
    norm_factor = 1.0 if z_count_total == 0 else v_characteristic / z_count_total
    z_density_norm = {k: v for k, v in zip(z_count.keys(), np.array(list(z_density.values())) * norm_factor)}

    results: dict[str, DensityProfile] = {
        "r_count": DensityProfile(r_count, f"Profile of {description} atom count vs radius, based on center of wetted area:"),
        "r_density": DensityProfile(r_density, f"Profile of {description} density (atoms/angstrom**3) vs radius, based on center of wetted area:"),
        "r_density_norm": DensityProfile(r_density_norm, f"Profile of {description} normalized density vs radius, based on center of wetted area:"),
        "z_count": DensityProfile(z_count, f"Profile of {description} atom count vs z:"),
        "z_density": DensityProfile(z_density, f"Profile of {description} density (atoms/angstrom**3) vs z, based on cylinder formed around wetted area:"),
        "z_density_norm": DensityProfile(z_density_norm, f"Profile of {description} normalized density vs z, based on cylinder formed around wetted area:"),
    }

    for k in range(len(z_bins) - 1):
        height_z_bin: float = z_bins[k + 1] - z_bins[k]
        atoms_z_bin: list[Atom] = [a for a in atoms_cyl if a.pos.z >= z_bins[k] and a.pos.z < z_bins[k + 1]]
        if k == len(z_bins) - 2: atoms_z_bin += [a for a in atoms_cyl if a.pos.z == z_bins[k + 1]]
        r_count_z = build_profile([math.sqrt((a.pos.x - x_wet)**2 + (a.pos.y - y_wet)**2) for a in atoms_z_bin], r_bins)
        r_bin_volumes_z = [math.pi * (r_bins[i + 1]**2 - r_bins[i]**2) * height_z_bin for i in range(len(r_bins) - 1)]
        r_density_z = {k: v for k, v in zip(r_count_z.keys(), [list(r_count_z.values())[i] / r_bin_volumes_z[i] for i in range(len(r_count_z))])}
        r_count_total_z = sum(r_count.values())
        norm_factor_z: float = 1.0 if r_count_total_z == 0 else v_characteristic / r_count_total_z
        r_density_norm_z = {k: v for k, v in zip(r_count_z.keys(), np.array(list(r_density_z.values())) * norm_factor_z)}
        suffix_name: str = f"_{z_bins[k]}_{z_bins[k + 1]}"
        # Can't use f-string for the line below because it mistakenly throws an error for an unclosed square bracket
        suffix_description: str = ", in z-range of [" + str(z_bins[k]) + ", " + str(z_bins[k + 1]) + ("]" if k == len(z_bins) - 2 else ")")
        results["r_count" + suffix_name] = DensityProfile(r_count_z, f"Profile of {description} atom count vs radius, based on droplet center of mass{suffix_description}:")
        results["r_density" + suffix_name] = DensityProfile(r_density_z, f"Profile of {description} density (atoms/angstrom**3) vs radius, based on droplet center of mass{suffix_description}:")
        results["r_density_norm" + suffix_name] = DensityProfile(r_density_norm_z, f"Profile of {description} normalized density vs radius, based on droplet center of mass{suffix_description}:")

    return results

def build_profiles_spherical(atoms: list[Atom], config: ConfigReader, droplet_com: Vector3D, description: str) -> dict[str, DensityProfile]:
    r_bins = build_bins_radial(config.spherical_profile_start_r, config.approx_sphere["R"], config.spherical_profile_step_r)
    r_count = build_profile([math.sqrt((atom.pos.x - droplet_com.x)**2 + (atom.pos.y - droplet_com.y)**2 + (atom.pos.z - droplet_com.z)**2) for atom in atoms], r_bins)

    r_bin_volumes = [four_thirds_pi * (r_bins[i + 1]**3 - r_bins[i]**3) for i in range(len(r_bins) - 1)]
    r_density = {k: v for k, v in zip(r_count.keys(), [list(r_count.values())[i] / r_bin_volumes[i] for i in range(len(r_count))])}

    r_count_total = sum(r_count.values())
    v_characteristic = four_thirds_pi * float(config.approx_sphere["R"])**3
    norm_factor = 1.0 if r_count_total == 0 else v_characteristic / r_count_total
    r_density_norm = {k: v for k, v in zip(r_count.keys(), np.array(list(r_density.values())) * norm_factor)}

    return {
        "r_count": DensityProfile(r_count, f"Profile of {description} atom count vs radius, based on droplet center of mass:"),
        "r_density": DensityProfile(r_density, f"Profile of {description} density (atoms/angstrom**3) vs radius, based on droplet center of mass:"),
        "r_density_norm": DensityProfile(r_density_norm, f"Profile of {description} normalized density vs radius, based on droplet center of mass:"),
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

def build_bins_radial(start: float, stop: float, step: float) -> ndarray[float]:
    bins = np.append([0.0], np.arange(start, stop, step)) # First bin is the central "core"
    if stop > bins[-1]: bins = np.append(bins, stop) # Append one last bin to cover the remainder (may be smaller than the other bins)
    return bins