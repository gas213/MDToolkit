import os.path
import sys

from md_analyses.atom_extremes import find_atom_extremes
from md_analyses.center_of_mass import calc_droplet_center
from md_analyses.density_profiles import build_density_profiles
from md_analyses.salt_concentration import calc_salt_concentration
from md_analyses.vapor_count import count_vapor_particles
from md_dataclasses.density_profile import DensityProfile
from md_readers.argv_reader import read_config_path
from md_readers.config_reader import ConfigReader
from md_readers.data_reader_mediator import read_header, read_atoms
from make_directories import make_directories
import printer

print("Reading config...")
config = ConfigReader(read_config_path(sys.argv))
print("Making directories...")
dir_results = make_directories(config.data_path)
print("Reading data header...")
header = read_header(config)
print("Reading atoms...")
atoms = read_atoms(config)
print("Finding atom extremes...")
atom_extremes = find_atom_extremes(atoms)
print("Calculating salt concentration...")
salt_concentration = calc_salt_concentration(config, atoms)
print("Counting vapor molecules...")
vapor_count = count_vapor_particles(config, atoms)
print("Calculating droplet center of mass...")
droplet_center = calc_droplet_center(config, atoms)
print("Building density profiles...")
density_profiles: dict[str, dict[str, DensityProfile]] = {
    "all_atom": build_density_profiles(config, header, atoms, droplet_center, 0, "all_atom"),
    "chlorine": build_density_profiles(config, header, atoms, droplet_center, 4, "chlorine"),
    "hydrogen": build_density_profiles(config, header, atoms, droplet_center, 7, "hydrogen"),
    "oxygen": build_density_profiles(config, header, atoms, droplet_center, 6, "oxygen"),
    "sodium": build_density_profiles(config, header, atoms, droplet_center, 5, "sodium"),
}

print("Writing output files...")
summary = ""
summary += printer.print_title(config.data_path)
summary += printer.print_header(header)
summary += printer.print_atom_extremes(atom_extremes)
summary += printer.print_sanity_checks(header, atom_extremes, atoms, density_profiles["all_atom"])
summary += printer.print_salt_concentration(salt_concentration)
summary += printer.print_vapor_count(vapor_count)
summary += printer.print_droplet_center(droplet_center)
with open(os.path.join(dir_results, "summary.txt"), "w") as analysis: analysis.write(summary)

for atom_name, profile_group in density_profiles.items():
    dir_atom = os.path.join(dir_results, f"profiles/{atom_name}")
    os.makedirs(dir_atom)
    for profile_name, profile in profile_group.items():
        with open(os.path.join(dir_atom, f"{profile_name}.txt"), "w") as out_file: out_file.write(printer.print_density_profile(profile))

print("ANALYSIS COMPLETE")