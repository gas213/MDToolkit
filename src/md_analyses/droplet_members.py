# from dataclasses import dataclass
# from multiprocessing import Manager, Pool
# from multiprocessing.managers import ListProxy, ValueProxy
# import numpy as np

# from constants import element_sets
# from md_dataclasses.atom import Atom
# from md_dataclasses.box import Box
# from md_dataclasses.header import Header
# from md_dataclasses.vector3d import Vector3D
# from md_readers.config_reader import ConfigReader

# WIDTH_PILLAR: float = 2.0 # Half-width of pillar sampling regions (in angstroms) when approximating droplet center point
# HEIGHT_SLAB: float = 1.0 # Half-height of slab sampling region (in angstroms) when approximating droplet center point

# BIN_SIZE: float = 40.0 # Size of the x-y-z sampling bins (in angstroms)

# def get_progress_step_size(atoms: list[Atom]) -> int:
#     """Returns an interval for how often to print progress updates (at least 1%) for a given list of atoms to process."""
#     return 1 if len(atoms) < 100 else int(float(len(atoms)) / 100.0)

# @dataclass
# class ProcessBinArgsOld1:
#     bin: Box
#     atoms_o_shared: ListProxy
#     threshold_shared: ValueProxy
#     id: int

# @dataclass
# class ProcessBinArgs:
#     bin: Box
#     atoms_o_local: list[Atom]
#     threshold: float
#     id: int

# def process_bin(args: ProcessBinArgs) -> list[Atom]:
#     print(f"Bin #{args.id} starting: " + str(bin))
#     threshold2: float = args.threshold**2
#     members_o_local: list[Atom] = []
#     atoms_o_bin = [o for o in args.atoms_o_local if
#                    o.pos.x > args.bin.lo.x and o.pos.x <= args.bin.hi.x and
#                    o.pos.y > args.bin.lo.y and o.pos.y <= args.bin.hi.y and
#                    o.pos.z > args.bin.lo.z and o.pos.z <= args.bin.hi.z]
#     for o_bin in atoms_o_bin:
#         for o_mem in members_o_local:
#             # Check one dimension at a time and bail as soon as it is too far away
#             d2: float = (o_bin.pos.x - o_mem.pos.x)**2
#             if d2 > threshold2: continue
#             d2 += (o_bin.pos.y - o_mem.pos.y)**2
#             if d2 > threshold2: continue
#             d2 += (o_bin.pos.z - o_mem.pos.z)**2
#             if d2 > threshold2: continue
#             o_bin.is_droplet_member = True
#             members_o_local.append(o_bin)
#             break
#         if o_bin.is_droplet_member: continue
#         counter_o: int = 0
#         for o_maybe in args.atoms_o_local:
#             if o_maybe.is_droplet_member: continue
#             # Check one dimension at a time and bail as soon as it is too far away
#             d2: float = (o_bin.pos.x - o_maybe.pos.x)**2
#             if d2 > threshold2: continue
#             d2 += (o_bin.pos.y - o_maybe.pos.y)**2
#             if d2 > threshold2: continue
#             d2 += (o_bin.pos.z - o_maybe.pos.z)**2
#             if d2 > threshold2: continue
#             if o_bin.id == o_maybe.id: continue
#             if counter_o >= 1:
#                 o_bin.is_droplet_member = True
#                 members_o_local.append(o_bin)
#                 break
#             else:
#                 counter_o += 1
#     print(f"Bin #{args.id} complete, {len(members_o_local)}/{len(atoms_o_bin)} oxygens are members.")
#     return atoms_o_bin

# def set_droplet_members(config: ConfigReader, header: Header, atoms: list[Atom]) -> None:
#     atoms_o: list[Atom] = [a for a in atoms if a.type in config.get_atom_type_ids(element_sets["oxygen"])]
#     threshold: float = config.droplet_member_threshold

#     # Create x-y-z sampling bins, uniformly-sized except for the bins along the xhi/yhi/zhi edges of the simulation box
#     bin_edges: list[list[float]] = [[], [], []]
#     for x in np.arange(header.box.lo.x, header.box.hi.x, BIN_SIZE): bin_edges[0].append(x)
#     for y in np.arange(header.box.lo.y, header.box.hi.y, BIN_SIZE): bin_edges[1].append(y)
#     for z in np.arange(header.box.lo.z, header.box.hi.z, BIN_SIZE): bin_edges[2].append(z)
#     bin_edges[0].append(header.box.hi.x)
#     bin_edges[1].append(header.box.hi.y)
#     bin_edges[2].append(header.box.hi.z)
#     bin_count: int = (len(bin_edges[0]) - 1) * (len(bin_edges[1]) - 1) * (len(bin_edges[2]) - 1)
#     process_bin_args: list[ProcessBinArgs] = []
#     counter: int = 0
#     for k in range(len(bin_edges[2]) - 1):
#         atoms_o_local_z: list[Atom] = [o for o in atoms_o if o.pos.z > bin_edges[2][k] - threshold and o.pos.z <= bin_edges[2][k + 1] + threshold]
#         for j in range(len(bin_edges[1]) - 1):
#             atoms_o_local_yz: list[Atom] = [o for o in atoms_o_local_z if o.pos.y > bin_edges[1][j] - threshold and o.pos.y <= bin_edges[1][j + 1] + threshold]
#             for i in range(len(bin_edges[0]) - 1):
#                 counter += 1
#                 print(f"Building oxygen bin {counter}/{bin_count} ({round(counter / float(bin_count) * 100.0)}%)", end="\r")
#                 bin: Box = Box(Vector3D(bin_edges[0][i], bin_edges[1][j], bin_edges[2][k]), Vector3D(bin_edges[0][i + 1], bin_edges[1][j + 1], bin_edges[2][k + 1]))
#                 atoms_o_local_xyz: list[Atom] = [o for o in atoms_o_local_yz if o.pos.x > bin_edges[0][i] - threshold and o.pos.x <= bin_edges[0][i + 1] + threshold]
#                 process_bin_args.append(ProcessBinArgs(bin, atoms_o_local_xyz, threshold, counter))

#     # Make a worker pool to process the oxygens in each bin and return the (updated) oxygen atoms from each bin
#     atoms_o_processed: list[Atom] = []
#     with Pool() as pool:
#         results: list[list[Atom]] = pool.map(process_bin, process_bin_args)
#         atoms_o_processed = [o for atoms_o_bin in results for o in atoms_o_bin]

#     # Rebuild the full list of oxygen atoms, including any that were out of bounds, and make sure they're all accounted for with no duplicates
#     atoms_o_baddies = [o for o in atoms_o if
#                        o.pos.x <= header.box.lo.x or o.pos.x > header.box.hi.x or
#                        o.pos.y <= header.box.lo.y or o.pos.y > header.box.hi.y or
#                        o.pos.z <= header.box.lo.z or o.pos.z > header.box.hi.z]
#     if len(atoms_o_processed) + len(atoms_o_baddies) != len(atoms_o):
#         raise ValueError(f"Expected {len(atoms_o)} oxygen atoms, but got {len(atoms_o_processed) + len(atoms_o_baddies)} after processing droplet members.")
#     atoms_o = atoms_o_processed + atoms_o_baddies
#     ids_o: set[int] = set()
#     for o in atoms_o:
#         if o.id in ids_o: raise ValueError(f"Duplicate oxygen atom ID {o.id} found after processing droplet members.")
#         ids_o.add(o.id)

#     # TODO: find salt and hydrogen droplet members and then rebuild full atoms list
#     vapor_o: list[Vector3D] = [o.pos for o in atoms_o if not o.is_droplet_member]
#     vapor_o_count: int = len(vapor_o)
#     breakpoint = 0

# def process_bin_old1(args: ProcessBinArgs):
#     bin: Box = args.bin
#     atoms_o_shared: ListProxy = args.atoms_o_shared
#     threshold: float = args.threshold_shared.value
#     threshold2: float = threshold**2
#     print(f"Bin #{args.id} starting: " + str(bin))
#     atoms_o_near = [o for o in atoms_o_shared if
#                     o.pos.x > bin.lo.x - threshold and o.pos.x <= bin.hi.x + threshold and
#                     o.pos.y > bin.lo.y - threshold and o.pos.y <= bin.hi.y + threshold and
#                     o.pos.z > bin.lo.z - threshold and o.pos.z <= bin.hi.z + threshold]
#     print(f"Bin #{args.id} done gathering atoms_o_near.")
#     # The bin's first oxygen members list starts as a list of known members within proximity of the bin, and grows as we find members in the current bin
#     members_o_local1 = [o for o in atoms_o_near if o.is_droplet_member]
#     print(f"Bin #{args.id} done gathering members_o_local.")
#     atoms_o_bin = [o for o in atoms_o_near if
#                     o.pos.x > bin.lo.x and o.pos.x <= bin.hi.x and
#                     o.pos.y > bin.lo.y and o.pos.y <= bin.hi.y and
#                     o.pos.z > bin.lo.z and o.pos.z <= bin.hi.z]
#     print(f"Bin #{args.id} done gathering atoms_o_bin.")
#     # First determine which oxygens in the current bin are in proximity to a solved member
#     for o_bin in atoms_o_bin:
#         for o_mem in members_o_local1:
#             # Check one dimension at a time and bail as soon as it is too far away
#             d2: float = (o_bin.pos.x - o_mem.pos.x)**2
#             if d2 > threshold2: continue
#             d2 += (o_bin.pos.y - o_mem.pos.y)**2
#             if d2 > threshold2: continue
#             d2 += (o_bin.pos.z - o_mem.pos.z)**2
#             if d2 > threshold2: continue
#             o_bin.is_droplet_member = True
#             members_o_local1.append(o_bin)
#             break
#     # For all remaining oxygens in the bin, check if they are close to at least two other undetermined oxygens
#     # As this is happening, form a list of new members found this way, and do a proximity check with this list first
#     atoms_o_bin_remaining = [o for o in atoms_o_bin if not o.is_droplet_member]
#     if len(atoms_o_bin_remaining) == 0: return
#     members_o_local2: list[Atom] = []
#     maybes_o_local = [o for o in atoms_o_near if not o.is_droplet_member]
#     for o_bin in atoms_o_bin_remaining:
#         for o_mem in members_o_local2:
#             # Check one dimension at a time and bail as soon as it is too far away
#             d2: float = (o_bin.pos.x - o_mem.pos.x)**2
#             if d2 > threshold2: continue
#             d2 += (o_bin.pos.y - o_mem.pos.y)**2
#             if d2 > threshold2: continue
#             d2 += (o_bin.pos.z - o_mem.pos.z)**2
#             if d2 > threshold2: continue
#             o_bin.is_droplet_member = True
#             members_o_local2.append(o_bin)
#             break
#         if o_bin.is_droplet_member: continue
#         counter_o: int = 0
#         for o_maybe in maybes_o_local:
#             if o_maybe.is_droplet_member: continue
#             # Check one dimension at a time and bail as soon as it is too far away
#             d2: float = (o_bin.pos.x - o_maybe.pos.x)**2
#             if d2 > threshold2: continue
#             d2 += (o_bin.pos.y - o_maybe.pos.y)**2
#             if d2 > threshold2: continue
#             d2 += (o_bin.pos.z - o_maybe.pos.z)**2
#             if d2 > threshold2: continue
#             if o_bin.id == o_maybe.id: continue
#             if counter_o >= 1:
#                 o_bin.is_droplet_member = True
#                 members_o_local2.append(o_bin)
#                 break
#             else:
#                 counter_o += 1
#     print(f"Bin #{args.id} complete.")

# def set_droplet_members_old5(config: ConfigReader, header: Header, atoms: list[Atom]) -> None:
#     manager = Manager()
#     atoms_o = [a for a in atoms if a.type in config.get_atom_type_ids(element_sets["oxygen"])]
#     atoms_o_shared = manager.list(atoms_o)
#     threshold_shared = manager.Value("f", config.droplet_member_threshold)

#     # Create x-y-z sampling bins, uniformly-sized except for the bins along the xhi/yhi/zhi edges of the simulation box
#     bin_edges: list[list[float]] = [[], [], []]
#     for x in np.arange(header.box.lo.x, header.box.hi.x, BIN_SIZE): bin_edges[0].append(x)
#     for y in np.arange(header.box.lo.y, header.box.hi.y, BIN_SIZE): bin_edges[1].append(y)
#     for z in np.arange(header.box.lo.z, header.box.hi.z, BIN_SIZE): bin_edges[2].append(z)
#     bin_edges[0].append(header.box.hi.x)
#     bin_edges[1].append(header.box.hi.y)
#     bin_edges[2].append(header.box.hi.z)
#     process_bin_args: list[ProcessBinArgs] = []
#     counter: int = 0
#     for k in range(len(bin_edges[2]) - 1):
#         for j in range(len(bin_edges[1]) - 1):
#             for i in range(len(bin_edges[0]) - 1):
#                 counter += 1
#                 process_bin_args.append(ProcessBinArgs(
#                     Box(Vector3D(bin_edges[0][i], bin_edges[1][j], bin_edges[2][k]), Vector3D(bin_edges[0][i + 1], bin_edges[1][j + 1], bin_edges[2][k + 1])),
#                     atoms_o_shared, threshold_shared, counter))

#     with Pool() as pool:
#         pool.map(process_bin, process_bin_args)
#     breakpoint = 0

# def set_droplet_members_old4(config: ConfigReader, header: Header, atoms: list[Atom]) -> None:
#     atoms_o: list[Atom] = [a for a in atoms if a.type in config.get_atom_type_ids(element_sets["oxygen"])]
#     threshold = config.droplet_member_threshold
#     threshold2 = threshold * threshold

#     # Create x-y-z sampling bins, uniformly-sized except for the bins along the xhi/yhi/zhi edges of the simulation box
#     bins: list[list[float]] = [[], [], []]
#     for x in np.arange(header.box.lo.x, header.box.hi.x, BIN_SIZE): bins[0].append(x)
#     for y in np.arange(header.box.lo.y, header.box.hi.y, BIN_SIZE): bins[1].append(y)
#     for z in np.arange(header.box.lo.z, header.box.hi.z, BIN_SIZE): bins[2].append(z)
#     bins[0].append(header.box.hi.x)
#     bins[1].append(header.box.hi.y)
#     bins[2].append(header.box.hi.z)
#     bin_count_real: int = (len(bins[0]) - 1) * (len(bins[1]) - 1) * (len(bins[2]) - 1)
#     progress: int = 0
#     for k in range(len(bins[2]) - 1):
#         for j in range(len(bins[1]) - 1):
#             for i in range(len(bins[0]) - 1):
#                 progress += 1
#                 print(f"Setting droplet members: oxygen in bin {progress}/{bin_count_real} ({round(progress / float(bin_count_real) * 100.0)}%)", end="\r")
#                 atoms_o_near = [o for o in atoms_o if
#                                 o.pos.x > bins[0][i] - threshold and o.pos.x <= bins[0][i + 1] + threshold and
#                                 o.pos.y > bins[1][j] - threshold and o.pos.y <= bins[1][j + 1] + threshold and
#                                 o.pos.z > bins[2][k] - threshold and o.pos.z <= bins[2][k + 1] + threshold]
#                 # The bin's first oxygen members list starts as a list of known members within proximity of the bin, and grows as we find members in the current bin
#                 members_o_local1 = [o for o in atoms_o_near if o.is_droplet_member]
#                 atoms_o_bin = [o for o in atoms_o_near if
#                                o.pos.x > bins[0][i] and o.pos.x <= bins[0][i + 1] and
#                                o.pos.y > bins[1][j] and o.pos.y <= bins[1][j + 1] and
#                                o.pos.z > bins[2][k] and o.pos.z <= bins[2][k + 1]]
#                 # First determine which oxygens in the current bin are in proximity to a solved member
#                 for o_bin in atoms_o_bin:
#                     for o_mem in members_o_local1:
#                         # Check one dimension at a time and bail as soon as it is too far away
#                         d2: float = (o_bin.pos.x - o_mem.pos.x)**2
#                         if d2 > threshold2: continue
#                         d2 += (o_bin.pos.y - o_mem.pos.y)**2
#                         if d2 > threshold2: continue
#                         d2 += (o_bin.pos.z - o_mem.pos.z)**2
#                         if d2 > threshold2: continue
#                         o_bin.is_droplet_member = True
#                         members_o_local1.append(o_bin)
#                         break
#                 # # Do a second pass for all remaining oxygens in the bin
#                 # atoms_o_bin_remaining = [o for o in atoms_o_bin if not o.is_droplet_member]
#                 # if len(atoms_o_bin_remaining) == 0: continue
#                 # for o_bin in atoms_o_bin_remaining:
#                 #     for o_mem in members_o_local1:
#                 #         # Check one dimension at a time and bail as soon as it is too far away
#                 #         d2: float = (o_bin.pos.x - o_mem.pos.x)**2
#                 #         if d2 > threshold2: continue
#                 #         d2 += (o_bin.pos.y - o_mem.pos.y)**2
#                 #         if d2 > threshold2: continue
#                 #         d2 += (o_bin.pos.z - o_mem.pos.z)**2
#                 #         if d2 > threshold2: continue
#                 #         o_bin.is_droplet_member = True
#                 #         members_o_local1.append(o_bin)
#                 #         break
#                 # For all remaining oxygens in the bin, check if they are close to at least two other undetermined oxygens
#                 # As this is happening, form a list of new members found this way, and do a proximity check with this list first
#                 atoms_o_bin_remaining = [o for o in atoms_o_bin if not o.is_droplet_member]
#                 if len(atoms_o_bin_remaining) == 0: continue
#                 members_o_local2: list[Atom] = []
#                 maybes_o_local = [o for o in atoms_o_near if not o.is_droplet_member]
#                 for o_bin in atoms_o_bin_remaining:
#                     for o_mem in members_o_local2:
#                         # Check one dimension at a time and bail as soon as it is too far away
#                         d2: float = (o_bin.pos.x - o_mem.pos.x)**2
#                         if d2 > threshold2: continue
#                         d2 += (o_bin.pos.y - o_mem.pos.y)**2
#                         if d2 > threshold2: continue
#                         d2 += (o_bin.pos.z - o_mem.pos.z)**2
#                         if d2 > threshold2: continue
#                         o_bin.is_droplet_member = True
#                         members_o_local2.append(o_bin)
#                         break
#                     if o_bin.is_droplet_member: continue
#                     counter_o: int = 0
#                     for o_maybe in maybes_o_local:
#                         if o_maybe.is_droplet_member: continue
#                         # Check one dimension at a time and bail as soon as it is too far away
#                         d2: float = (o_bin.pos.x - o_maybe.pos.x)**2
#                         if d2 > threshold2: continue
#                         d2 += (o_bin.pos.y - o_maybe.pos.y)**2
#                         if d2 > threshold2: continue
#                         d2 += (o_bin.pos.z - o_maybe.pos.z)**2
#                         if d2 > threshold2: continue
#                         if o_bin.id == o_maybe.id: continue
#                         if counter_o >= 1:
#                             o_bin.is_droplet_member = True
#                             members_o_local2.append(o_bin)
#                             break
#                         else:
#                             counter_o += 1

#     test = sum(1 for o in atoms_o if not o.is_droplet_member)
#     breakpoint = 0

# def set_droplet_members_old3(config: ConfigReader, header: Header, atoms: list[Atom]) -> None:
#     atoms_o: list[Atom] = [a for a in atoms if a.type in config.get_atom_type_ids(element_sets["oxygen"])]
#     threshold = config.droplet_member_threshold
#     threshold2 = threshold * threshold

#     # Create x-y-z sampling bins, uniformly-sized except for the bins along the xhi/yhi/zhi edges of the simulation box
#     # Include ghost bins on all sides of the simulation box
#     bins: list[list[float]] = [[header.box.lo.x - threshold], [header.box.lo.y - threshold], [header.box.lo.z - threshold]]
#     for x in np.arange(header.box.lo.x, header.box.hi.x, threshold): bins[0].append(x)
#     for y in np.arange(header.box.lo.y, header.box.hi.y, threshold): bins[1].append(y)
#     for z in np.arange(header.box.lo.z, header.box.hi.z, threshold): bins[2].append(z)
#     bins[0].extend([header.box.hi.x, header.box.hi.x + threshold])
#     bins[1].extend([header.box.hi.y, header.box.hi.y + threshold])
#     bins[2].extend([header.box.hi.z, header.box.hi.z + threshold])
#     bin_count_real: int = (len(bins[0]) - 3) * (len(bins[1]) - 3) * (len(bins[2]) - 3)
#     progress: int = 0
#     for k in range(1, len(bins[2]) - 2):
#         for j in range(1, len(bins[1]) - 2):
#             for i in range(1, len(bins[0]) - 2):
#                 progress += 1
#                 print(f"Setting droplet members: oxygen in bin {progress}/{bin_count_real} ({round(progress / float(bin_count_real) * 100.0)}%)", end="\r")
#                 atoms_o_near = [o for o in atoms_o if
#                                 o.pos.x > bins[0][i - 1] and o.pos.x <= bins[0][i + 2] and
#                                 o.pos.y > bins[1][j - 1] and o.pos.y <= bins[1][j + 2] and
#                                 o.pos.z > bins[2][k - 1] and o.pos.z <= bins[2][k + 2]]
#                 # The bin's first oxygen members list starts as a list of members from solved neighboring bins, but grows as we find members in the current bin
#                 members_o_near1 = [o for o in atoms_o_near if o.is_droplet_member]
#                 atoms_o_bin = [o for o in atoms_o_near if
#                                o.pos.x > bins[0][i] and o.pos.x <= bins[0][i + 1] and
#                                o.pos.y > bins[1][j] and o.pos.y <= bins[1][j + 1] and
#                                o.pos.z > bins[2][k] and o.pos.z <= bins[2][k + 1]]
#                 # First determine which oxygens in the current bin are sufficiently close to a solved member
#                 for o_bin in atoms_o_bin:
#                     for o_mem in members_o_near1:
#                         # Check one dimension at a time and bail as soon as it is too far away
#                         d2: float = (o_bin.pos.x - o_mem.pos.x)**2
#                         if d2 > threshold2: continue
#                         d2 += (o_bin.pos.y - o_mem.pos.y)**2
#                         if d2 > threshold2: continue
#                         d2 += (o_bin.pos.z - o_mem.pos.z)**2
#                         if d2 > threshold2: continue
#                         o_bin.is_droplet_member = True
#                         members_o_near1.append(o_bin)
#                         break
#                 # For all remaining oxygens in the bin, check if they are close to at least two other undetermined oxygens
#                 # As this is happening, form a list of new members found this way, and do a proximity check with this list first
#                 atoms_o_bin_remaining = [o for o in atoms_o_bin if not o.is_droplet_member]
#                 members_o_near2: list[Atom] = []
#                 maybes_o_near = [o for o in atoms_o_near if not o.is_droplet_member]
#                 for o_bin in atoms_o_bin_remaining:
#                     for o_mem in members_o_near2:
#                         # Check one dimension at a time and bail as soon as it is too far away
#                         d2: float = (o_bin.pos.x - o_mem.pos.x)**2
#                         if d2 > threshold2: continue
#                         d2 += (o_bin.pos.y - o_mem.pos.y)**2
#                         if d2 > threshold2: continue
#                         d2 += (o_bin.pos.z - o_mem.pos.z)**2
#                         if d2 > threshold2: continue
#                         o_bin.is_droplet_member = True
#                         members_o_near2.append(o_bin)
#                         break
#                     if o_bin.is_droplet_member: continue
#                     counter_o: int = 0
#                     for o_maybe in maybes_o_near:
#                         if o_maybe.is_droplet_member: continue
#                         # Check one dimension at a time and bail as soon as it is too far away
#                         d2: float = (o_bin.pos.x - o_maybe.pos.x)**2
#                         if d2 > threshold2: continue
#                         d2 += (o_bin.pos.y - o_maybe.pos.y)**2
#                         if d2 > threshold2: continue
#                         d2 += (o_bin.pos.z - o_maybe.pos.z)**2
#                         if d2 > threshold2: continue
#                         if o_bin.id == o_maybe.id: continue
#                         if counter_o >= 1:
#                             o_bin.is_droplet_member = True
#                             members_o_near2.append(o_bin)
#                             break
#                         else:
#                             counter_o += 1

#     test = sum(1 for o in atoms_o if not o.is_droplet_member)
#     breakpoint = 0

# def set_droplet_members_old2(config: ConfigReader, header: Header, atoms: list[Atom]) -> None:
#     oxygen_type_ids = config.get_atom_type_ids(element_sets["oxygen"])
#     threshold = config.droplet_member_threshold
#     threshold2 = threshold * threshold

#     # Create x-wise sampling bins: left (already processed), center (currently processing), and right (not yet processed)
#     # Bins are uniformly sized except for the last bin inside the box, which stops at the box's xhi
#     # Include a ghost bin on each side of the simulation box
#     x_bins: list[float] = [header.box.lo.x - threshold]
#     for x in np.arange(header.box.lo.x, header.box.hi.x, threshold): x_bins.append(x)
#     x_bins.append(header.box.hi.x)
#     x_bins.append(header.box.hi.x + threshold)
#     bin_count_real: int = len(x_bins) - 3

#     for i in range(1, len(x_bins) - 2):
#         x_left: float = x_bins[i - 1]
#         x_leftmid: float = x_bins[i]
#         x_rightmid: float = x_bins[i + 1]
#         x_right: float = x_bins[i + 2]
#         # The first oxygen members list starts as a list of members in the left bin, but grows as we find members in the middle bin
#         oxygen_members_pt1 = [atom for atom in atoms if atom.is_droplet_member and atom.type in oxygen_type_ids and atom.pos.x > x_left and atom.pos.x <= x_leftmid]
#         oxygen_middle = [atom for atom in atoms if atom.type in oxygen_type_ids and atom.pos.x > x_leftmid and atom.pos.x <= x_rightmid]
#         oxygen_right = [atom for atom in atoms if atom.type in oxygen_type_ids and atom.pos.x > x_rightmid and atom.pos.x <= x_right]
#         progress_step: int = get_progress_step_size(oxygen_middle)
#         progress: int = 0
#         len1 = len(oxygen_members_pt1) # TODO: remove these lines
#         len2 = len(oxygen_middle)
#         len3 = len(oxygen_right)
#         breakpoint = 0
#         # First determine which oxygens in the middle bin are sufficiently close to an existing member
#         for o_mid in oxygen_middle:
#             if progress % progress_step == 0:
#                 print(f"Setting droplet members: oxygen in bin {i}/{bin_count_real}, part 1/2, {round(progress / float(len(oxygen_middle)) * 100.0)}%", end="\r")
#             progress += 1
#             for o_mem in oxygen_members_pt1:
#                 # Check one dimension at a time and bail as soon as it is too far away
#                 # Check z and y first because we already know x has a good chance of being close
#                 d2: float = (o_mid.pos.z - o_mem.pos.z)**2
#                 if d2 > threshold2: continue
#                 d2 += (o_mid.pos.y - o_mem.pos.y)**2
#                 if d2 > threshold2: continue
#                 d2 += (o_mid.pos.x - o_mem.pos.x)**2
#                 if d2 > threshold2: continue
#                 o_mid.is_droplet_member = True
#                 oxygen_members_pt1.append(o_mid)
#                 break
#         # For all remaining oxygens in the middle bin, check if they are close to at least two other undetermined oxygens
#         # As this is happening, form a list of new members found this way, and do a proximity check with this list first
#         oxygen_middle_remaining = [oxygen for oxygen in oxygen_middle if not oxygen.is_droplet_member]
#         oxygen_members_pt2: list[Atom] = []
#         oxygen_midright = oxygen_middle_remaining + oxygen_right
#         progress_step = get_progress_step_size(oxygen_middle_remaining)
#         progress = 0
#         len4 = len(oxygen_middle_remaining) # TODO: remove these lines
#         len5 = len(oxygen_midright)
#         breakpoint = 0
#         for o_mid in oxygen_middle_remaining:
#             if progress % progress_step == 0:
#                 print(f"Setting droplet members: oxygen in bin {i}/{bin_count_real}, part 2/2, {round(progress / float(len(oxygen_middle_remaining)) * 100.0)}%", end="\r")
#             progress += 1
#             for o_mem in oxygen_members_pt2:
#                 # Check one dimension at a time and bail as soon as it is too far away
#                 # Check z and y first because we already know x has a good chance of being close
#                 d2: float = (o_mid.pos.z - o_mem.pos.z)**2
#                 if d2 > threshold2: continue
#                 d2 += (o_mid.pos.y - o_mem.pos.y)**2
#                 if d2 > threshold2: continue
#                 d2 += (o_mid.pos.x - o_mem.pos.x)**2
#                 if d2 > threshold2: continue
#                 o_mid.is_droplet_member = True
#                 oxygen_members_pt2.append(o_mid)
#                 break
#             if o_mid.is_droplet_member: continue
#             nearby_oxygens: int = 0
#             for o_midright in oxygen_midright:
#                 if o_midright.is_droplet_member: continue
#                 # Check one dimension at a time and bail as soon as it is too far away
#                 # Check z and y first because we already know x has a good chance of being close
#                 d2: float = (o_mid.pos.z - o_midright.pos.z)**2
#                 if d2 > threshold2: continue
#                 d2 += (o_mid.pos.y - o_midright.pos.y)**2
#                 if d2 > threshold2: continue
#                 d2 += (o_mid.pos.x - o_midright.pos.x)**2
#                 if d2 > threshold2: continue
#                 if o_mid.id == o_midright.id: continue
#                 if nearby_oxygens >= 1:
#                     o_mid.is_droplet_member = True
#                     oxygen_members_pt2.append(o_mid)
#                     break
#                 else:
#                     nearby_oxygens += 1

#     test = sum(1 for atom in atoms if not atom.is_droplet_member and atom.type in oxygen_type_ids)
#     breakpoint = 0

# def set_droplet_members_old1(config: ConfigReader, header: Header, atoms: list[Atom]) -> None:
#     hydrogen_type_ids = config.get_atom_type_ids(element_sets["hydrogen"])
#     oxygen_type_ids = config.get_atom_type_ids(element_sets["oxygen"])
#     salt_type_ids = config.get_atom_type_ids(element_sets["salt"])
#     saltwater_type_ids = config.get_atom_type_ids(element_sets["saltwater"])
#     threshold = config.droplet_member_threshold
#     threshold2 = threshold * threshold
#     progress_step_all: int = 1 if len(atoms) < 100 else int(float(len(atoms)) / 100.0)
#     atoms_oxygen = [atom for atom in atoms if atom.type in oxygen_type_ids] # Pre-populated list to avoid repeated type checks
#     members_oxygen: list[Atom] = []
    
#     # Use x-y center of box, and the average z-position of droplet atoms near this line, as an initial guess for the droplet's center point
#     com_guess = Vector3D(0.5 * (header.box.lo.x + header.box.hi.x), 0.5 * (header.box.lo.y + header.box.hi.y), 0.0)
#     z_numerator: float = 0.0
#     z_denominator: float = 0.0
#     for atom in atoms:
#         # Sample within a narrow vertical square pillar region that runs along the x-y center of the box
#         if atom.type in saltwater_type_ids and abs(atom.pos.x - com_guess.x) <= WIDTH_PILLAR and abs(atom.pos.y - com_guess.y) <= WIDTH_PILLAR:
#             z_numerator += atom.pos.z
#             z_denominator += 1.0
#     com_guess.z = z_numerator / z_denominator if z_denominator > 0.0 else 0.0

#     # Find a better approximation for the x-y center of the droplet by sampling within an x-y slab region near the z-guess
#     com_approx = Vector3D(0.0, 0.0, 0.0)
#     x_numerator: float = 0.0
#     y_numerator: float = 0.0
#     xy_denominator: float = 0.0
#     for atom in atoms:
#         if atom.type in saltwater_type_ids and abs(atom.pos.z - com_guess.z) <= HEIGHT_SLAB:
#             x_numerator += atom.pos.x
#             y_numerator += atom.pos.y
#             xy_denominator += 1.0
#     com_approx.x = x_numerator / xy_denominator if xy_denominator > 0.0 else com_guess.x
#     com_approx.y = y_numerator / xy_denominator if xy_denominator > 0.0 else com_guess.y

#     # Find a better approximation for the z-center of the droplet by creating a new pillar region and doing a proximity check for real droplet members
#     atoms_pillar: list[Atom] = [atom for atom in atoms if abs(atom.pos.x - com_approx.x) <= WIDTH_PILLAR and abs(atom.pos.y - com_approx.y) <= WIDTH_PILLAR]
#     atoms_pillar_salt = [atom for atom in atoms_pillar if atom.type in salt_type_ids]
#     atoms_pillar_oxygen = [atom for atom in atoms_pillar if atom.type in oxygen_type_ids]
#     atoms_pillar_hydrogen = [atom for atom in atoms_pillar if atom.type in hydrogen_type_ids]
#     progress_step_salt: int = 1 if len(atoms_pillar_salt) < 100 else int(float(len(atoms_pillar_salt)) / 100.0)
#     progress_step_oxygen: int = 1 if len(atoms_pillar_oxygen) < 100 else int(float(len(atoms_pillar_oxygen)) / 100.0)
#     progress_step_hydrogen: int = 1 if len(atoms_pillar_hydrogen) < 100 else int(float(len(atoms_pillar_hydrogen)) / 100.0)
#     progress: int = 0
#     pillar_margin_xlo = com_approx.x - WIDTH_PILLAR - threshold
#     pillar_margin_xhi = com_approx.x + WIDTH_PILLAR + threshold
#     pillar_margin_ylo = com_approx.y - WIDTH_PILLAR - threshold
#     pillar_margin_yhi = com_approx.y + WIDTH_PILLAR + threshold
#     d2: float = 0.0
#     # Process salt atoms first - they should all be droplet members
#     for atom in atoms_pillar_salt:
#         if progress % progress_step_salt == 0: print(f"Setting droplet members: central pillar... salt {round(progress / float(len(atoms_pillar_salt)) * 100.0)}%", end="\r")
#         progress += 1
#         atom.is_droplet_member = True
#     # Process oxygen atoms via proximity checks with other oxygens
#     progress = 0
#     for o1 in atoms_pillar_oxygen:
#         if progress % progress_step_oxygen == 0: print(f"Setting droplet members: central pillar... salt 100%, oxygen {round(progress / float(len(atoms_pillar_oxygen)) * 100.0)}%", end="\r")
#         progress += 1
#         # First check if this oxygen atom is close to any oxygen atom that is already determined to be a droplet member
#         for o2 in members_oxygen:
#             # Check one dimension at a time and bail as soon as it is too far away
#             d2 = (o1.pos.x - o2.pos.x)**2
#             if d2 > threshold2: continue
#             d2 += (o1.pos.y - o2.pos.y)**2
#             if d2 > threshold2: continue
#             d2 += (o1.pos.z - o2.pos.z)**2
#             if d2 > threshold2: continue
#             o1.is_droplet_member = True
#             members_oxygen.append(o1)
#             break
#         # If still undetermined, check if there are at least two other undetermined oxygens nearby
#         if not o1.is_droplet_member:
#             nearby_oxygens: int = 0
#             for o2 in atoms_oxygen:
#                 if not o2.is_droplet_member:
#                     # Start with simple checks to see if it is too far away from the pillar
#                     if o2.pos.x < pillar_margin_xlo or o2.pos.x > pillar_margin_xhi or o2.pos.y < pillar_margin_ylo or o2.pos.y > pillar_margin_yhi: continue
#                     # Since we kind of already checked x and y, check z next
#                     d2 = (o1.pos.z - o2.pos.z)**2
#                     if d2 > threshold2: continue
#                     # Check the full distance if we made it this far
#                     d2 += (o1.pos.x - o2.pos.x)**2 + (o1.pos.y - o2.pos.y)**2
#                     if d2 > threshold2: continue
#                     if o1.id == o2.id: continue
#                     if nearby_oxygens >= 1:
#                         o1.is_droplet_member = True
#                         members_oxygen.append(o1)
#                         break
#                     else:
#                         nearby_oxygens += 1
#                         continue
#     # Now process hydrogen atoms via proximity checks with oxygen atoms that are already droplet members
#     # Doing it this way because the molecule IDs can't be trusted
#     progress = 0
#     for h in atoms_pillar_hydrogen:
#         if progress % progress_step_hydrogen == 0: print(f"Setting droplet members: central pillar... salt 100%, oxygen 100%, hydrogen {round(progress / float(len(atoms_pillar_hydrogen)) * 100.0)}%", end="\r")
#         progress += 1
#         for o in members_oxygen:
#             d2 = (h.pos.x - o.pos.x)**2
#             if d2 > threshold2: continue
#             d2 += (h.pos.y - o.pos.y)**2
#             if d2 > threshold2: continue
#             d2 += (h.pos.z - o.pos.z)**2
#             if d2 > threshold2: continue
#             h.is_droplet_member = True
#             break
#     print("Setting droplet members: central pillar... salt 100%, oxygen 100%, hydrogen 100%")
#     # Find z-range and midpoint of the droplet members in the pillar region
#     zlo_pillar_members: float = com_guess.z
#     zhi_pillar_members: float = com_guess.z
#     for atom in atoms_pillar:
#         if atom.is_droplet_member and atom.pos.z < zlo_pillar_members: zlo_pillar_members = atom.pos.z
#         if atom.is_droplet_member and atom.pos.z > zhi_pillar_members: zhi_pillar_members = atom.pos.z
#     com_approx.z = 0.5 * (zlo_pillar_members + zhi_pillar_members)

#     # Define spherical region that comprises most of the droplet internals, based on the approximate center and z-range
#     # Label all atoms within this sphere as droplet members
#     # Keep the edge of the sphere inside of the z-range by at least 3 angstroms to avoid including vapor atoms
#     r2_sphere: float = min(0.98 * (zhi_pillar_members - com_approx.z), zhi_pillar_members - com_approx.z - 3.0)**2
#     progress = 0
#     for atom in atoms:
#         if progress % progress_step_all == 0: print(f"Setting droplet members: central sphere... {round(progress / float(len(atoms)) * 100.0)}%", end="\r")
#         progress += 1
#         if not atom.is_droplet_member:
#             d2 = (atom.pos.x - com_approx.x)**2
#             if d2 > r2_sphere: continue
#             d2 += (atom.pos.y - com_approx.y)**2
#             if d2 > r2_sphere: continue
#             d2 += (atom.pos.z - com_approx.z)**2
#             if d2 > r2_sphere: continue
#             atom.is_droplet_member = True
#             if atom.type in oxygen_type_ids: members_oxygen.append(atom)
#     print("Setting droplet members: central sphere... 100%")

#     # Process the rest of the salt atoms
#     progress = 0
#     for atom in atoms:
#         if progress % progress_step_all == 0: print(f"Setting droplet members: remaining salt... {round(progress / float(len(atoms)) * 100.0)}%", end="\r")
#         progress += 1
#         if not atom.is_droplet_member and atom.type in salt_type_ids: atom.is_droplet_member = True
#     print("Setting droplet members: remaining salt... 100%")

#     # Process the rest of the oxygen atoms
#     atoms_oxygen_remaining: list[Atom] = [atom for atom in atoms if atom.type in oxygen_type_ids and not atom.is_droplet_member]
#     progress_step_oxygen = 1 if len(atoms_oxygen_remaining) < 100 else int(float(len(atoms_oxygen_remaining)) / 100.0)
#     progress = 0
#     for o1 in atoms_oxygen_remaining:
#         if progress % progress_step_oxygen == 0: print(f"Setting droplet members: remaining oxygen... {round(progress / float(len(atoms_oxygen_remaining)) * 100.0)}%", end="\r")
#         progress += 1
#         # First check if this oxygen atom is close to any oxygen atom that is already determined to be a droplet member
#         for o2 in members_oxygen:
#             # Check one dimension at a time and bail as soon as it is too far away
#             d2 = (o1.pos.x - o2.pos.x)**2
#             if d2 > threshold2: continue
#             d2 += (o1.pos.y - o2.pos.y)**2
#             if d2 > threshold2: continue
#             d2 += (o1.pos.z - o2.pos.z)**2
#             if d2 > threshold2: continue
#             o1.is_droplet_member = True
#             members_oxygen.append(o1)
#             break
#         # If still undetermined, check if there are at least two other undetermined oxygens nearby
#         if not o1.is_droplet_member:
#             nearby_oxygens: int = 0
#             for o2 in atoms_oxygen_remaining:
#                 if not o2.is_droplet_member:
#                     d2 = (o1.pos.x - o2.pos.x)**2
#                     if d2 > threshold2: continue
#                     d2 += (o1.pos.y - o2.pos.y)**2
#                     if d2 > threshold2: continue
#                     d2 += (o1.pos.z - o2.pos.z)**2
#                     if d2 > threshold2: continue
#                     if o1.id == o2.id: continue
#                     if nearby_oxygens >= 1:
#                         o1.is_droplet_member = True
#                         members_oxygen.append(o1)
#                         break
#                     else:
#                         nearby_oxygens += 1
#                         continue
#     print("Setting droplet members: remaining oxygen... 100%")

#     # Process the rest of the hydrogen atoms
#     progress = 0
#     for atom in atoms:
#         if progress % progress_step_all == 0: print(f"Setting droplet members: remaining hydrogen... {round(progress / float(len(atoms)) * 100.0)}%", end="\r")
#         progress += 1
#         if atom.is_droplet_member or atom.type not in hydrogen_type_ids: continue
#         for o in members_oxygen:
#             d2 = (atom.pos.x - o.pos.x)**2
#             if d2 > threshold2: continue
#             d2 += (atom.pos.y - o.pos.y)**2
#             if d2 > threshold2: continue
#             d2 += (atom.pos.z - o.pos.z)**2
#             if d2 > threshold2: continue
#             atom.is_droplet_member = True
#             break
#     print("Setting droplet members: remaining hydrogen... 100%")