import math

from constants import min_radius_for_radial_profiles, four_thirds_pi
from md_dataclasses.density_profile import DensityProfileGroup

def build_density_profiles(config, header, atoms, droplet_center, atom_type = 0):
    x_c = droplet_center.x
    y_c = droplet_center.y
    z_c = droplet_center.z
    x = dict()
    y = dict()
    z = dict()
    r_count = dict()
    r_density = dict()
    r_density_norm = dict()
    for val in range(int(header.box.lo.x), int(header.box.hi.x) + 1): x[val] = 0
    for val in range(int(header.box.lo.y), int(header.box.hi.y) + 1): y[val] = 0
    for val in range(int(header.box.lo.z), int(header.box.hi.z) + 1): z[val] = 0
    for val in range(min_radius_for_radial_profiles, int(config.approx_sphere["R"])): r_count[val] = 0
    for val in range(min_radius_for_radial_profiles, int(config.approx_sphere["R"])): r_density[val] = 0
    for val in range(min_radius_for_radial_profiles, int(config.approx_sphere["R"])): r_density_norm[val] = 0
    
    for atom in atoms:
        if (atom_type == 0 or atom.type == atom_type):
            x[int(atom.pos.x)] += 1
            y[int(atom.pos.y)] += 1
            z[int(atom.pos.z)] += 1

            r_atom = math.sqrt((atom.pos.x - x_c)**2 + (atom.pos.y - y_c)**2 + (atom.pos.z - z_c)**2)
            if int(r_atom) in r_count: r_count[int(r_atom)] += 1

    r_count_total = sum(r_count.values())
    v_total = four_thirds_pi * float(config.approx_sphere["R"])**3
    norm_factor = v_total / r_count_total

    v_inner = four_thirds_pi * float(min_radius_for_radial_profiles)**3
    for r_inner in range(min_radius_for_radial_profiles, int(config.approx_sphere["R"])):
        v_outer = four_thirds_pi * float(r_inner + 1)**3
        r_density[r_inner] = float(r_count[r_inner]) / (v_outer - v_inner)
        r_density_norm[r_inner] = r_density[r_inner] * norm_factor
        v_inner = v_outer

    return DensityProfileGroup(x, y, z, r_count, r_density, r_density_norm)