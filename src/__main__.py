import os.path
import sys

from md_analyses.atom_extremes import find_atom_extremes
from md_analyses.center_of_mass import calc_droplet_center
from md_analyses.density_profiles import build_density_profiles
from md_analyses.salt_concentration import calc_salt_concentration
from md_analyses.vapor_count import count_vapor_particles
from md_readers.argv_reader import read_config_path
from md_readers.config_reader import ConfigReader
from md_readers.reader_manager import read_header, read_atoms
from make_directories import make_directories
import printer

config = ConfigReader(read_config_path(sys.argv))
dir_write = make_directories(config.data_path)
header = read_header(config.data_path)
atoms = read_atoms(config.data_path)
atom_extremes = find_atom_extremes(atoms)
salt_concentration = calc_salt_concentration(config, atoms)
vapor_count = count_vapor_particles(config, atoms)
droplet_center = calc_droplet_center(config, atoms)
atom_count_profiles = build_density_profiles(config, header, atoms, droplet_center)
chlorine_count_profiles = build_density_profiles(config, header, atoms, droplet_center, 4)
sodium_count_profiles = build_density_profiles(config, header, atoms, droplet_center, 5)
oxygen_count_profiles = build_density_profiles(config, header, atoms, droplet_center, 6)
hydrogen_count_profiles = build_density_profiles(config, header, atoms, droplet_center, 7)

results = ""
results += printer.print_title(config.data_path)
results += printer.print_header(header)
results += printer.print_atom_extremes(atom_extremes)
results += printer.print_sanity_checks(header, atom_extremes, atoms, atom_count_profiles)
results += printer.print_salt_concentration(salt_concentration)
results += printer.print_vapor_count(vapor_count)
results += printer.print_droplet_center(droplet_center)
results += printer.print_density_profiles(atom_count_profiles, "all-atom")
results += printer.print_density_profiles(chlorine_count_profiles, "chlorine")
results += printer.print_density_profiles(sodium_count_profiles, "sodium")
results += printer.print_density_profiles(oxygen_count_profiles, "oxygen")
results += printer.print_density_profiles(hydrogen_count_profiles, "hydrogen")

with open(os.path.join(dir_write, "summary.txt"), "w") as analysis: analysis.write(results)

print("Analysis complete")