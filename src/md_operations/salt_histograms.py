from md_domain.atom import Atom
from md_domain.salt_histogram import SaltHistogram
from md_enums.salt_type import SaltType

def build_salt_histograms(atoms: list[Atom], type_na: int, type_cl: int, r_threshold: float) -> tuple[SaltHistogram, SaltHistogram]:
    atoms_na = [atom for atom in atoms if atom.type == type_na]
    atoms_cl = [atom for atom in atoms if atom.type == type_cl]

    if len(atoms_na) == 0:
        raise Exception("No sodium atoms found when building salt histograms.")
    if len(atoms_cl) == 0:
        raise Exception("No chlorine atoms found when building salt histograms.")
    
    histogram_na_centric = SaltHistogram(SaltType.SODIUM, build_histogram_data(atoms_na, atoms_cl, r_threshold))
    histogram_cl_centric = SaltHistogram(SaltType.CHLORINE, build_histogram_data(atoms_cl, atoms_na, r_threshold))

    return histogram_na_centric, histogram_cl_centric

def build_histogram_data(atoms_center: list[Atom], atoms_neighbor: list[Atom], r_threshold: float) -> dict[int, float]:
    r_threshold_2 = r_threshold ** 2
    data: dict[int, float] = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0, 7: 0.0}

    for atom_center in atoms_center:
        neighbor_count: int = sum(1 for atom_neighbor in atoms_neighbor if (atom_center.pos.x - atom_neighbor.pos.x)**2 + (atom_center.pos.y - atom_neighbor.pos.y)**2 + (atom_center.pos.z - atom_neighbor.pos.z)**2 <= r_threshold_2)
        if neighbor_count not in data:
            raise Exception(f"Unexpected number of neighbor ions when building salt histogram: {neighbor_count}")
        data[neighbor_count] += 1

    normalizer: float = 1.0 / len(atoms_center)
    for key in data.keys():
        data[key] *= normalizer
    
    return data