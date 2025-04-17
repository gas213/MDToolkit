from constants import atom_type_groups

def count_vapor_particles(config, atoms):
    x0 = config.approx_sphere["X"]
    y0 = config.approx_sphere["Y"]
    z0 = config.approx_sphere["Z"]
    r2 = config.approx_sphere["R"]**2
    result = 0
    for atom in atoms:
        if (atom.type in atom_type_groups["oxygen"] and ((atom.pos.x - x0)**2 + (atom.pos.y - y0)**2 + (atom.pos.z - z0)**2) > r2):
            result += 1

    return result