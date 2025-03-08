import sys

from argvReader import read_data_path
from constants import box_vapor
from dumpFileReader import read_header, read_atoms
import sanityChecks
import writer

config = {
    "data path": read_data_path(sys.argv)
}

config.update(read_header(config["data path"]))

atom_results = read_atoms(config["data path"], config["box"], box_vapor)

sanity_checks = {}
sanity_checks = sanityChecks.atoms_within_box(sanity_checks, config, atom_results["atom extremes"])
sanity_checks = sanityChecks.total_atom_count(sanity_checks, config, atom_results["atom counter"])
sanity_checks = sanityChecks.density_profile_atom_count(sanity_checks, config, atom_results["density profiles"])

writer.write(config, atom_results["atom extremes"], atom_results["density profiles"], sanity_checks, atom_results["vapor counter"])

print("Analysis complete")