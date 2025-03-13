import math

from constants import approximation_sphere, min_radius_for_density_profiles
from named_tuples import DensityProfileGroup

def build_density_profiles(header, atoms, droplet_center):
    x_c = droplet_center.x
    y_c = droplet_center.y
    z_c = droplet_center.z
    x = dict()
    y = dict()
    z = dict()
    r = dict()
    for val in range(int(header.box.xlo), int(header.box.xhi) + 1): x[val] = 0
    for val in range(int(header.box.ylo), int(header.box.yhi) + 1): y[val] = 0
    for val in range(int(header.box.zlo), int(header.box.zhi) + 1): z[val] = 0
    for val in range(min_radius_for_density_profiles, int(approximation_sphere["r"])): r[val] = 0
    
    for atom in atoms:
        if int(atom.x) in x: x[int(atom.x)] += 1
        if int(atom.y) in y: y[int(atom.y)] += 1
        if int(atom.z) in z: z[int(atom.z)] += 1

        r_atom = math.sqrt((atom.x - x_c)**2 + (atom.y - y_c)**2 + (atom.z - z_c)**2)
        if int(r_atom) in r: r[int(r_atom)] += 1

    return DensityProfileGroup(x, y, z, r)