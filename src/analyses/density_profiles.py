from named_tuples import DensityProfileGroup

def build_density_profiles(header, atoms):
    x = dict()
    y = dict()
    z = dict()
    for val in range(int(header.box.xlo), int(header.box.xhi) + 1): x[val] = 0
    for val in range(int(header.box.ylo), int(header.box.yhi) + 1): y[val] = 0
    for val in range(int(header.box.zlo), int(header.box.zhi) + 1): z[val] = 0
    
    for atom in atoms:
        if int(atom.x) in x: x[int(atom.x)] += 1
        if int(atom.y) in y: y[int(atom.y)] += 1
        if int(atom.z) in z: z[int(atom.z)] += 1

    return DensityProfileGroup(x, y, z)