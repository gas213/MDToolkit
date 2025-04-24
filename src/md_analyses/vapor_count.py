from md_dataclasses.atom import Atom
from md_readers.config_reader import ConfigReader

def count_vapor_particles(config: ConfigReader, atoms: list[Atom]) -> int:
    x0 = config.approx_sphere["X"]
    y0 = config.approx_sphere["Y"]
    z0 = config.approx_sphere["Z"]
    r2 = config.approx_sphere["R"]**2
    vapor_count = 0
    atom_types_oxygen = config.get_atom_type_ids(["O"])
    for atom in atoms:
        if (atom.type in atom_types_oxygen and ((atom.pos.x - x0)**2 + (atom.pos.y - y0)**2 + (atom.pos.z - z0)**2) > r2):
            vapor_count += 1

    return vapor_count