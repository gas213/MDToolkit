import sys

from analyses.atom_extremes import find_atom_extremes
from analyses.center_of_mass import calc_droplet_center
from analyses.density_profiles import build_density_profiles
from analyses.vapor_count import count_vapor_particles
from readers.argv_reader import read_data_path
from readers.atoms_reader import atoms_from_dump_txt
from readers.header_reader import header_from_dump_txt
from constants import analysis_filetype
import printer

data_path = read_data_path(sys.argv)
header = header_from_dump_txt(data_path)
atoms = atoms_from_dump_txt(data_path)
atom_extremes = find_atom_extremes(atoms)
vapor_count = count_vapor_particles(atoms)
droplet_center = calc_droplet_center(atoms)
atom_count_profiles = build_density_profiles(header, atoms, droplet_center)
chlorine_count_profiles = build_density_profiles(header, atoms, droplet_center, 4)
sodium_count_profiles = build_density_profiles(header, atoms, droplet_center, 5)
oxygen_count_profiles = build_density_profiles(header, atoms, droplet_center, 6)
hydrogen_count_profiles = build_density_profiles(header, atoms, droplet_center, 7)

results = ""
results += printer.print_title(data_path)
results += printer.print_header(header)
results += printer.print_atom_extremes(atom_extremes)
results += printer.print_sanity_checks(header, atom_extremes, atoms, atom_count_profiles)
results += printer.print_vapor_count(vapor_count)
results += printer.print_droplet_center(droplet_center)
results += printer.print_density_profiles(atom_count_profiles, "atom")
results += printer.print_density_profiles(chlorine_count_profiles, "chlorine")
results += printer.print_density_profiles(sodium_count_profiles, "sodium")
results += printer.print_density_profiles(oxygen_count_profiles, "oxygen")
results += printer.print_density_profiles(hydrogen_count_profiles, "hydrogen")

with open(data_path + analysis_filetype, "w") as analysis: analysis.write(results)

print("Analysis complete")