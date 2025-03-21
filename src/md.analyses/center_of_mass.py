from constants import approximation_sphere, masses
from md_dataclasses.vector3d import Vector3D

def calc_droplet_center(atoms):
    x0 = approximation_sphere["x"]
    y0 = approximation_sphere["y"]
    z0 = approximation_sphere["z"]
    r2 = approximation_sphere["r"]**2
    sum_x = 0.0
    sum_y = 0.0
    sum_z = 0.0
    sum_m = 0.0
    for atom in atoms:
        if ((atom.x - x0)**2 + (atom.y - y0)**2 + (atom.z - z0)**2) <= r2:
            m = masses[atom.type]
            sum_x += m * atom.x
            sum_y += m * atom.y
            sum_z += m * atom.z
            sum_m += m
    
    return Vector3D(sum_x / sum_m, sum_y / sum_m, sum_z / sum_m)