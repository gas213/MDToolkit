from md_domain.atom import Atom

def build_first_neighbor_histogram_data(atoms_center: list[Atom], atoms_neighbor: list[Atom], r_threshold: float) -> dict[int, float]:    
    r_threshold_2 = r_threshold ** 2
    data: dict[int, float] = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0, 7: 0.0}

    for atom_center in atoms_center:
        neighbor_count: int = sum(1 for atom_neighbor in atoms_neighbor if (atom_center.pos.x - atom_neighbor.pos.x)**2 + (atom_center.pos.y - atom_neighbor.pos.y)**2 + (atom_center.pos.z - atom_neighbor.pos.z)**2 <= r_threshold_2)
        if neighbor_count not in data:
            raise Exception(f"Unexpected number of neighbor atoms when building first neighbor histogram: {neighbor_count}")
        data[neighbor_count] += 1

    normalizer: float = 1.0 / len(atoms_center)
    for key in data.keys():
        data[key] *= normalizer
    
    return data