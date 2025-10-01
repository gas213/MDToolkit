import netCDF4 as nc

from md_dataclasses.atom import Atom
from md_dataclasses.box import Box
from md_dataclasses.header import Header
from md_dataclasses.vector3d import Vector3D

# I don't know the purpose of "frame" yet
# Maybe this would have more than one value if you have multiple time steps in a single dump file?
frame = 0

def read_header(data_file: str) -> Header:
    dataset = nc.Dataset(data_file, "r")
    atom_count = len(dataset.variables["id"][frame])
    cell_origin = dataset.variables["cell_origin"][frame] # Origin coordinates of the simulation box (x, y, z)
    cell_lengths = dataset.variables["cell_lengths"][frame] # Side lengths of the simulation box (x, y, z)
    box_lo = Vector3D(cell_origin[0], cell_origin[1], cell_origin[2])
    box_hi = Vector3D(cell_origin[0] + cell_lengths[0], cell_origin[1] + cell_lengths[1], cell_origin[2] + cell_lengths[2])
    return Header(atom_count, Box(box_lo, box_hi))

def read_atoms(data_file: str) -> list[Atom]:
    dataset = nc.Dataset(data_file, "r")
    ids = dataset.variables["id"][frame]
    types = dataset.variables["type"][frame]
    coords = dataset.variables["coordinates"][frame]
    
    atoms: list[Atom] = [None] * len(ids)
    for index, id in enumerate(ids):
        atoms[index] = Atom(id, types[index], Vector3D(coords[index][0], coords[index][1], coords[index][2]))

    return atoms