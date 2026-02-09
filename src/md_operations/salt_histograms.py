from md_dataclasses.atom import Atom

R_THRESHOLD_2: float = 16.0 # Angstroms ^ 2
CL_TYPE: int = 4 # TODO: hardcoded for now
NA_TYPE: int = 5 # TODO: hardcoded for now

def build_cl_neighbors_histogram(atoms: list[Atom]) -> dict[int, int]:
    # TODO: don't generate these atom lists more than necessary
    atoms_cl = [atom for atom in atoms if atom.type == CL_TYPE]
    atoms_na = [atom for atom in atoms if atom.type == NA_TYPE]

    if len(atoms_na) == 0:
        raise Exception("No Na atoms found when building histogram of neighboring Cl")

    histogram: dict[int, float] = {
        0: 0.0,
        1: 0.0,
        2: 0.0,
        3: 0.0,
        4: 0.0,
        5: 0.0,
        6: 0.0,
        7: 0.0,
    }

    for atom_na in atoms_na:
        neighbor_count: int = sum(1 for atom_cl in atoms_cl if (atom_na.pos.x - atom_cl.pos.x)**2 + (atom_na.pos.y - atom_cl.pos.y)**2 + (atom_na.pos.z - atom_cl.pos.z)**2 <= R_THRESHOLD_2)
        if neighbor_count not in histogram:
            raise Exception(f"Unexpected number of Cl neighbors for Na atom: {neighbor_count}")
        histogram[neighbor_count] += 1

    normalizer: float = 1.0 / len(atoms_na)
    for key in histogram.keys():
        histogram[key] *= normalizer

    return histogram

def build_na_neighbors_histogram(atoms: list[Atom]) -> dict[int, int]:
    # TODO: don't generate these atom lists more than necessary
    atoms_cl = [atom for atom in atoms if atom.type == CL_TYPE]
    atoms_na = [atom for atom in atoms if atom.type == NA_TYPE]

    if len(atoms_cl) == 0:
        raise Exception("No Cl atoms found when building histogram of neighboring Na")

    histogram: dict[int, float] = {
        0: 0.0,
        1: 0.0,
        2: 0.0,
        3: 0.0,
        4: 0.0,
        5: 0.0,
        6: 0.0,
        7: 0.0,
    }

    for atom_cl in atoms_cl:
        neighbor_count: int = sum(1 for atom_na in atoms_na if (atom_cl.pos.x - atom_na.pos.x)**2 + (atom_cl.pos.y - atom_na.pos.y)**2 + (atom_cl.pos.z - atom_na.pos.z)**2 <= R_THRESHOLD_2)
        if neighbor_count not in histogram:
            raise Exception(f"Unexpected number of Na neighbors for Cl atom: {neighbor_count}")
        histogram[neighbor_count] += 1

    normalizer: float = 1.0 / len(atoms_cl)
    for key in histogram.keys():
        histogram[key] *= normalizer

    return histogram