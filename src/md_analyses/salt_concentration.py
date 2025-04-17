def calc_salt_concentration(config, atoms):
    x0 = config.approx_sphere["X"]
    y0 = config.approx_sphere["Y"]
    z0 = config.approx_sphere["Z"]
    r2 = config.approx_sphere["R"]**2
    m_salt = 0.0
    m_saltwater = 0.0
    atom_types_saltwater = config.get_atom_type_ids(["Cl", "H", "Na", "O"])
    atom_types_salt = config.get_atom_type_ids(["Cl", "Na"])
    for atom in atoms:
        if atom.type in atom_types_saltwater and ((atom.pos.x - x0)**2 + (atom.pos.y - y0)**2 + (atom.pos.z - z0)**2) <= r2:
            m_saltwater += config.mass_lookup[atom.type]
            if atom.type in atom_types_salt:
                m_salt += config.mass_lookup[atom.type]

    return m_salt / m_saltwater