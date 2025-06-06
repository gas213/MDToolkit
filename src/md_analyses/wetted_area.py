import copy
from dataclasses import dataclass
import math
from multiprocessing import Pool
import numpy as np

from constants import BIN_SIZE, element_sets, WORKER_COUNT
from md_dataclasses.atom import Atom
from md_dataclasses.box import Box
from md_dataclasses.vector3d import Vector3D
from md_readers.config_reader import ConfigReader

@dataclass
class ProcessBinArgs:
    bin: Box
    liq_bin: list[Atom]
    ptfe_local: list[Atom]
    threshold: float

def calc_wetted_area(config: ConfigReader, atoms: list[Atom]) -> dict[str, float]:
    threshold: float = config.wetting_threshold
    atoms_liquid: list[Atom] = \
        [a for a in atoms if a.type in config.get_atom_type_ids(element_sets["salt"])] + \
        [a for a in atoms if a.type in config.get_atom_type_ids(element_sets["oxygen"]) and not a.is_vapor]
    atoms_ptfe: list[Atom] = [a for a in atoms if a.type in config.get_atom_type_ids(element_sets["ptfe"])]
    
    # First determine an approximate wetting region, anything outside of this can be ruled out immediately
    box_approx = Box(copy.deepcopy(atoms_liquid[0].pos), copy.deepcopy(atoms_liquid[0].pos))
    for liq in atoms_liquid:
        box_approx.lo.x = min(box_approx.lo.x, liq.pos.x)
        box_approx.hi.x = max(box_approx.hi.x, liq.pos.x)
        box_approx.lo.y = min(box_approx.lo.y, liq.pos.y)
        box_approx.hi.y = max(box_approx.hi.y, liq.pos.y)
        box_approx.lo.z = min(box_approx.lo.z, liq.pos.z)
    box_approx.lo.x -= threshold
    box_approx.hi.x += threshold
    box_approx.lo.y -= threshold
    box_approx.hi.y += threshold
    box_approx.lo.z -= threshold
    box_approx.hi.z = max([ptfe.pos.z for ptfe in atoms_ptfe]) + threshold

    # Create x-y-z sampling bins, uniformly-sized except for the bins with the highest x/y/z
    bin_edges: list[list[float]] = [[], [], []]
    for x in np.arange(box_approx.lo.x, box_approx.hi.x, BIN_SIZE): bin_edges[0].append(x)
    for y in np.arange(box_approx.lo.y, box_approx.hi.y, BIN_SIZE): bin_edges[1].append(y)
    for z in np.arange(box_approx.lo.z, box_approx.hi.z, BIN_SIZE): bin_edges[2].append(z)
    bin_edges[0].append(box_approx.hi.x)
    bin_edges[1].append(box_approx.hi.y)
    bin_edges[2].append(box_approx.hi.z)
    bin_count: int = (len(bin_edges[0]) - 1) * (len(bin_edges[1]) - 1) * (len(bin_edges[2]) - 1)
    process_bin_args: list[ProcessBinArgs] = []
    counter: int = 0
    for k in range(len(bin_edges[2]) - 1):
        liq_bin_z: list[Atom] = [liq for liq in atoms_liquid if liq.pos.z > bin_edges[2][k] and liq.pos.z <= bin_edges[2][k + 1]]
        ptfe_local_z: list[Atom] = [ptfe for ptfe in atoms_ptfe if ptfe.pos.z > bin_edges[2][k] - threshold and ptfe.pos.z <= bin_edges[2][k + 1] + threshold]
        for j in range(len(bin_edges[1]) - 1):
            liq_bin_yz: list[Atom] = [liq for liq in liq_bin_z if liq.pos.y > bin_edges[1][j] and liq.pos.y <= bin_edges[1][j + 1]]
            ptfe_local_yz: list[Atom] = [ptfe for ptfe in ptfe_local_z if ptfe.pos.y > bin_edges[1][j] - threshold and ptfe.pos.y <= bin_edges[1][j + 1] + threshold]
            for i in range(len(bin_edges[0]) - 1):
                counter += 1
                print(f"Building sampling bin {counter}/{bin_count} ({round(counter / float(bin_count) * 100.0)}%)", end="\r")
                bin: Box = Box(Vector3D(bin_edges[0][i], bin_edges[1][j], bin_edges[2][k]), Vector3D(bin_edges[0][i + 1], bin_edges[1][j + 1], bin_edges[2][k + 1]))
                liq_bin_xyz: list[Atom] = [liq for liq in liq_bin_yz if liq.pos.x > bin_edges[0][i] and liq.pos.x <= bin_edges[0][i + 1]]
                ptfe_local_xyz: list[Atom] = [ptfe for ptfe in ptfe_local_yz if ptfe.pos.x > bin_edges[0][i] - threshold and ptfe.pos.x <= bin_edges[0][i + 1] + threshold]
                process_bin_args.append(ProcessBinArgs(bin, liq_bin_xyz, ptfe_local_xyz, threshold))

    # Make a worker pool to process the liquid atoms in each bin and return the IDs of those that are in proximity to PTFE
    results: list[list[Vector3D]] = []
    with Pool(WORKER_COUNT) as pool:
        counter: int = 0
        count: int = len(process_bin_args)
        interval: int = 1 if count < 100 else int(count / float(100))
        for result in pool.imap_unordered(process_bin, process_bin_args):
            counter += 1
            results.append(result)
            if counter % interval == 0: print(f"Determining wetted area... {int(counter / float(count) * 100)}%", end="\r")
    
    wetted_positions = [pos for result in results for pos in result]
    x_avg: float = 0.0
    y_avg: float = 0.0
    counter: int = 0
    for pos in wetted_positions:
        counter += 1
        div_factor: float = 1.0 / float(counter)
        x_avg = (x_avg * float(counter - 1) + pos.x) * div_factor
        y_avg = (y_avg * float(counter - 1) + pos.y) * div_factor
    r2_max_xy: float = 0.0
    for pos in wetted_positions:
        r2_max_xy = max(r2_max_xy, (pos.x - x_avg)**2 + (pos.y - y_avg)**2)
    print(f"Determining wetted area... 100%")
    return {"x": x_avg, "y": y_avg, "r": math.sqrt(r2_max_xy)}

def process_bin(args: ProcessBinArgs) -> list[Vector3D]:
    threshold2: float = args.threshold**2
    wetted_positions: list[Vector3D] = []
    for liq in args.liq_bin:
        for ptfe in args.ptfe_local:
            # Check one dimension at a time and bail as soon as it is too far away
            d2: float = (liq.pos.x - ptfe.pos.x)**2
            if d2 > threshold2: continue
            d2 += (liq.pos.y - ptfe.pos.y)**2
            if d2 > threshold2: continue
            d2 += (liq.pos.z - ptfe.pos.z)**2
            if d2 > threshold2: continue
            wetted_positions.append(liq.pos)
            break
    return wetted_positions