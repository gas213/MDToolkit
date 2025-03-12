import datetime
import sys

from analyses.density_profiles import build_density_profiles
from readers.argv_reader import read_data_path
from readers.atoms_reader import atoms_from_dump_txt
from readers.header_reader import header_from_dump_txt
from constants import analysis_filetype
from sanityChecks import find_atom_extremes, atoms_within_box, total_atom_count, density_profile_atom_count
# from readers.atoms_reader import from_dump_txt
# from constants import sphere_vapor
# from dumpFileReader import read_header, read_atoms
# import sanityChecks
# import writer

data_path = read_data_path(sys.argv)
header = header_from_dump_txt(data_path)
atoms = atoms_from_dump_txt(data_path)
atom_extremes = find_atom_extremes(atoms)
density_profiles = build_density_profiles(header, atoms)

results = "ANALYSIS OF DATA FILE LOCATED AT: " + data_path
results += "\nPerformed: " + str(datetime.datetime.now())
results += "\n\nHeader data:"
for name, val in header._asdict().items(): results += "\n" + name + ": " + str(val)
results += "\n\nMost extreme atom coordinates:"
results += "\n" + str(atom_extremes)
results += "\n\nSanity checks:"
results += "\n" + atoms_within_box(header.box, atom_extremes)
results += "\n" + total_atom_count(header, len(atoms))
results += "\n" + density_profile_atom_count(header, density_profiles)
results += "\n\nProfile of atom density (count) by truncated x coordinate:"
for key, val in density_profiles.x.items(): results += "\n" + str(key) + ": " + str(val)
results += "\n\nProfile of atom density (count) by truncated y coordinate:"
for key, val in density_profiles.y.items(): results += "\n" + str(key) + ": " + str(val)
results += "\n\nProfile of atom density (count) by truncated z coordinate:"
for key, val in density_profiles.z.items(): results += "\n" + str(key) + ": " + str(val)

with open(data_path + analysis_filetype, "w") as analysis: analysis.write(results)

# config = {
#     "data path": read_data_path(sys.argv)
# }

# config.update(read_header(config["data path"]))

# atom_results = read_atoms(config["data path"], config["box"], sphere_vapor)

# sanity_checks = {}
# sanity_checks = sanityChecks.atoms_within_box(sanity_checks, config, atom_results["atom extremes"])
# sanity_checks = sanityChecks.total_atom_count(sanity_checks, config, atom_results["atom counter"])
# sanity_checks = sanityChecks.density_profile_atom_count(sanity_checks, config, atom_results["density profiles"])

# writer.write(config, atom_results["atom extremes"], atom_results["density profiles"], sanity_checks, atom_results["vapor counter"])

print("Analysis complete")