import datetime
import sys

from readers.argv_reader import read_data_path
from readers.atoms_reader import atoms_from_dump_txt
from readers.header_reader import header_from_dump_txt
from constants import analysis_filetype
# from readers.atoms_reader import from_dump_txt
# from constants import sphere_vapor
# from dumpFileReader import read_header, read_atoms
# import sanityChecks
# import writer

data_path = read_data_path(sys.argv)
header = header_from_dump_txt(data_path)
atoms = atoms_from_dump_txt(data_path)

results = "ANALYSIS OF DATA FILE LOCATED AT: " + data_path + "\n"
results += "Performed: " + str(datetime.datetime.now()) + "\n"
results += "\nHeader data:\n\n"
for name, val in header._asdict().items(): results += name + ": " + str(val) + "\n"

with open(data_path + analysis_filetype, "w") as analysis:
    analysis.write(results)

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