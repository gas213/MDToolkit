import math

from constants import approximation_sphere, min_radius_for_radial_profiles
from named_tuples import ProfileGroup

def build_atom_count_profiles(header, atoms, droplet_center, atom_type = 0):
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
    for val in range(min_radius_for_radial_profiles, int(approximation_sphere["r"])): r[val] = 0
    
    for atom in atoms:
        if (atom_type == 0 or atom.type == atom_type):
            x[int(atom.x)] += 1
            y[int(atom.y)] += 1
            z[int(atom.z)] += 1

            r_atom = math.sqrt((atom.x - x_c)**2 + (atom.y - y_c)**2 + (atom.z - z_c)**2)
            if int(r_atom) in r: r[int(r_atom)] += 1

    return ProfileGroup(x, y, z, r)