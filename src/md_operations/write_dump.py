from md_domain.atom import Atom
from md_domain.box import Box

def write_dump(write_path: str, box: Box, step: int, atoms: list[Atom]):
    with open(write_path, "w") as file:
        file.write("ITEM: TIMESTEP\n")
        file.write(f"{step}\n")
        file.write("ITEM: NUMBER OF ATOMS\n")
        file.write(f"{len(atoms)}\n")
        file.write("ITEM: BOX BOUNDS pp pp pp\n")
        file.write(f"{box.lo.x} {box.hi.x}\n")
        file.write(f"{box.lo.y} {box.hi.y}\n")
        file.write(f"{box.lo.z} {box.hi.z}\n")
        file.write("ITEM: ATOMS id type x y z\n")
        file.write("\n".join([f"{atom.id} {atom.type} {atom.pos.x} {atom.pos.y} {atom.pos.z}" for atom in atoms]))