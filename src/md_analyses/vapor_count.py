from constants import approximation_sphere, atom_type_groups

def count_vapor_particles(atoms):
    x0 = approximation_sphere["x"]
    y0 = approximation_sphere["y"]
    z0 = approximation_sphere["z"]
    r2 = approximation_sphere["r"]**2
    result = 0
    for atom in atoms:
        if (atom.type in atom_type_groups["oxygen"] and ((atom.pos.x - x0)**2 + (atom.pos.y - y0)**2 + (atom.pos.z - z0)**2) > r2):
            result += 1

    return result