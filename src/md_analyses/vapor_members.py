from dataclasses import dataclass
from multiprocessing import Pool
import numpy as np
import os

from constants import element_sets
from md_dataclasses.atom import Atom
from md_dataclasses.box import Box
from md_dataclasses.header import Header
from md_dataclasses.vector3d import Vector3D
from md_readers.config_reader import ConfigReader

WORKER_COUNT: int = max(os.cpu_count() - 2, 1) # Number of workers to use in multiprocessing pool
BIN_SIZE: float = 40.0 # Size of the x-y-z sampling bins, in angstroms

@dataclass
class ProcessBinArgs:
    bin: Box
    atoms_o_local: list[Atom]
    threshold: float

def determine_vapor(config: ConfigReader, header: Header, atoms: list[Atom]) -> None:
    atoms_dict: dict[int, Atom] = {}
    for atom in atoms:
        if atom.id in atoms_dict: raise Exception(f"Encountered duplicate atom ID {atom.id}")
        atoms_dict[atom.id] = atom

    atoms_o: list[Atom] = [a for a in atoms_dict.values() if a.type in config.get_atom_type_ids(element_sets["oxygen"])]
    threshold: float = config.vapor_threshold

    # Create x-y-z sampling bins, uniformly-sized except for the bins along the xhi/yhi/zhi edges of the simulation box
    bin_edges: list[list[float]] = [[], [], []]
    for x in np.arange(header.box.lo.x, header.box.hi.x, BIN_SIZE): bin_edges[0].append(x)
    for y in np.arange(header.box.lo.y, header.box.hi.y, BIN_SIZE): bin_edges[1].append(y)
    for z in np.arange(header.box.lo.z, header.box.hi.z, BIN_SIZE): bin_edges[2].append(z)
    bin_edges[0].append(header.box.hi.x)
    bin_edges[1].append(header.box.hi.y)
    bin_edges[2].append(header.box.hi.z)
    bin_count: int = (len(bin_edges[0]) - 1) * (len(bin_edges[1]) - 1) * (len(bin_edges[2]) - 1)
    process_bin_args: list[ProcessBinArgs] = []
    counter: int = 0
    for k in range(len(bin_edges[2]) - 1):
        atoms_o_local_z: list[Atom] = [o for o in atoms_o if o.pos.z > bin_edges[2][k] - threshold and o.pos.z <= bin_edges[2][k + 1] + threshold]
        for j in range(len(bin_edges[1]) - 1):
            atoms_o_local_yz: list[Atom] = [o for o in atoms_o_local_z if o.pos.y > bin_edges[1][j] - threshold and o.pos.y <= bin_edges[1][j + 1] + threshold]
            for i in range(len(bin_edges[0]) - 1):
                counter += 1
                print(f"Building oxygen bin {counter}/{bin_count} ({round(counter / float(bin_count) * 100.0)}%)", end="\r")
                bin: Box = Box(Vector3D(bin_edges[0][i], bin_edges[1][j], bin_edges[2][k]), Vector3D(bin_edges[0][i + 1], bin_edges[1][j + 1], bin_edges[2][k + 1]))
                atoms_o_local_xyz: list[Atom] = [o for o in atoms_o_local_yz if o.pos.x > bin_edges[0][i] - threshold and o.pos.x <= bin_edges[0][i + 1] + threshold]
                process_bin_args.append(ProcessBinArgs(bin, atoms_o_local_xyz, threshold))

    # Make a worker pool to process the oxygens in each bin and return the IDs of vapor atoms
    results: list[set] = []
    with Pool(WORKER_COUNT) as pool:
        counter: int = 0
        count: int = len(process_bin_args)
        interval: int = 1 if count < 100 else int(count / float(100))
        for result in pool.imap_unordered(process_bin, process_bin_args):
            counter += 1
            results.append(result)
            if counter % interval == 0: print(f"Determining vapor atoms (oxygen)... {int(counter / float(count) * 100)}%", end="\r")
    for result in results:
        for vapor_o_id in result:
            atoms_dict[vapor_o_id].is_vapor = True
    print(f"Setting droplet members: oxygen... 100%")

def process_bin(args: ProcessBinArgs) -> set[int]:
    threshold2: float = args.threshold**2
    liquid_o_bin: list[Atom] = []
    atoms_o_bin = [o for o in args.atoms_o_local if
                   o.pos.x > args.bin.lo.x and o.pos.x <= args.bin.hi.x and
                   o.pos.y > args.bin.lo.y and o.pos.y <= args.bin.hi.y and
                   o.pos.z > args.bin.lo.z and o.pos.z <= args.bin.hi.z]
    # Since this function is intended to be called in a worker pool, any changes to this property are intended only for the scope of the function
    for o_bin in args.atoms_o_local: o_bin.is_vapor = True # True until proven false
    for o_bin in atoms_o_bin:
        for o_liq in liquid_o_bin:
            # Check one dimension at a time and bail as soon as it is too far away
            d2: float = (o_bin.pos.x - o_liq.pos.x)**2
            if d2 > threshold2: continue
            d2 += (o_bin.pos.y - o_liq.pos.y)**2
            if d2 > threshold2: continue
            d2 += (o_bin.pos.z - o_liq.pos.z)**2
            if d2 > threshold2: continue
            liquid_o_bin.append(o_bin)
            o_bin.is_vapor = False
            break
        if not o_bin.is_vapor: continue
        counter_o: int = 0
        for o_maybe in args.atoms_o_local:
            if not o_maybe.is_vapor: continue
            # Check one dimension at a time and bail as soon as it is too far away
            d2: float = (o_bin.pos.x - o_maybe.pos.x)**2
            if d2 > threshold2: continue
            d2 += (o_bin.pos.y - o_maybe.pos.y)**2
            if d2 > threshold2: continue
            d2 += (o_bin.pos.z - o_maybe.pos.z)**2
            if d2 > threshold2: continue
            if o_bin.id == o_maybe.id: continue
            if counter_o >= 1:
                liquid_o_bin.append(o_bin)
                o_bin.is_vapor = False
                break
            else:
                counter_o += 1
    return set([o.id for o in atoms_o_bin if o.is_vapor])