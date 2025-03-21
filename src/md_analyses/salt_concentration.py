from constants import approximation_sphere, atom_type_groups, masses

def calc_salt_concentration(atoms):
    x0 = approximation_sphere["x"]
    y0 = approximation_sphere["y"]
    z0 = approximation_sphere["z"]
    r2 = approximation_sphere["r"]**2
    m_salt = 0.0
    m_saltwater = 0.0
    for atom in atoms:
        if atom.type in atom_type_groups["saltwater"] and ((atom.x - x0)**2 + (atom.y - y0)**2 + (atom.z - z0)**2) <= r2:
            m_saltwater += masses[atom.type]
            if atom.type in atom_type_groups["salt"]:
                m_salt += masses[atom.type]

    return m_salt / m_saltwater