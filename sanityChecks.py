def atoms_within_box(sanity_checks, config, atom_extremes):
    name = "All atoms positioned within box"

    if (atom_extremes["x"][0] > config["box"]["xlo"] and
        atom_extremes["x"][1] < config["box"]["xhi"] and
        atom_extremes["y"][0] > config["box"]["ylo"] and
        atom_extremes["y"][1] < config["box"]["yhi"] and
        atom_extremes["z"][0] > config["box"]["zlo"] and
        atom_extremes["z"][1] < config["box"]["zhi"]):
        sanity_checks[name] = True
    else:
        sanity_checks[name] = False

    return sanity_checks

def total_atom_count(sanity_checks, config, atom_counter):
    name = "Count of atom rows matches total atom count"

    if atom_counter == config["total atoms"]: sanity_checks[name] = True
    else: sanity_checks[name] = False

    return sanity_checks

def density_profile_atom_count(sanity_checks, config, density_profiles):
    for axis in ["x", "y", "z"]:
        name = axis.upper() + " density profile accounts for all atoms"
        if sum(density_profiles[axis].values()) == config["total atoms"]: sanity_checks[name] = True
        else: sanity_checks[name] = False

    return sanity_checks