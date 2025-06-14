import copy
import os.path
import sys

from constants import element_sets
from file_writer import FileWriter
from md_analyses.atom_extremes import find_atom_extremes
from md_analyses.center_of_mass import calc_droplet_center
from md_analyses.density_profiles import build_profiles_cartesian, build_profiles_cylindrical, build_profiles_spherical
from md_analyses.salt_concentration import calc_salt_concentration
from md_analyses.time_aggregator import update_atom_extremes, update_avg_scalar, update_avg_profile
from md_analyses.vapor_count import count_vapor_particles
from md_analyses.vapor_members import determine_vapor
from md_analyses.wetted_area import calc_wetted_area
from md_dataclasses.box import Box
from md_dataclasses.density_profile import DensityProfile
from md_dataclasses.vector3d import Vector3D
from md_readers.argv_reader import read_config_path
from md_readers.config_reader import ConfigReader
from md_readers.data_reader_mediator import read_header, read_atoms
import text_printer as tp

print("Reading config and making directories...")
config = ConfigReader(read_config_path(sys.argv))
file_counter = 0
file_count = len(config.data_files)
file_writer = FileWriter(config)
file_writer.mkdirs_initial()

print("Reading header of first data file...")
header = read_header(config, config.data_files[0])

atom_extremes_overall: Box = None
salt_concentration_avg: float = 0.0
vapor_count_avg: float = 0.0
droplet_com_avg: Vector3D = Vector3D(0.0, 0.0, 0.0)
profiles_cartesian : dict[str, dict[str, DensityProfile]] = {}
profiles_cylindrical: dict[str, dict[str, DensityProfile]] = {}
profiles_spherical : dict[str, dict[str, DensityProfile]] = {}
profiles_cartesian_avg: dict[str, dict[str, DensityProfile]] = {}
profiles_cylindrical_avg: dict[str, dict[str, DensityProfile]] = {}
profiles_spherical_avg: dict[str, dict[str, DensityProfile]] = {}

for data_file in config.data_files:
    file_counter += 1
    print(f"Begin processing data file {file_counter}/{file_count}: {os.path.basename(data_file)}")

    print("Reading atoms...")
    atoms = read_atoms(config, data_file)

    wetted_area: dict[str, float] = {}
    if __name__ == "__main__": # Safety requirement for multiprocessing?
        determine_vapor(config, header, atoms)
        if config.enable_wetted_area: wetted_area = calc_wetted_area(config, atoms)

    if config.enable_atom_extremes:
        print("Finding atom extremes...")
        atom_extremes = find_atom_extremes(atoms)
        atom_extremes_overall = update_atom_extremes(atom_extremes_overall, atom_extremes)

    if config.enable_salt_concentration:
        print("Calculating salt concentration...")
        salt_concentration = calc_salt_concentration(config, atoms)
        salt_concentration_avg = update_avg_scalar(salt_concentration_avg, salt_concentration, file_counter)

    if config.enable_vapor_count:
        print("Counting vapor molecules...")
        vapor_count = count_vapor_particles(config, atoms)
        vapor_count_avg = update_avg_scalar(vapor_count_avg, vapor_count, file_counter)

    if config.enable_droplet_com:
        print("Calculating droplet center of mass...")
        droplet_com = calc_droplet_center(config, atoms)
        droplet_com_avg.x = update_avg_scalar(droplet_com_avg.x, droplet_com.x, file_counter)
        droplet_com_avg.y = update_avg_scalar(droplet_com_avg.y, droplet_com.y, file_counter)
        droplet_com_avg.z = update_avg_scalar(droplet_com_avg.z, droplet_com.z, file_counter)

    if config.enable_cartesian_profiles:
        print("Building cartesian profiles...")
        for element_name, elements in element_sets.items():
            profiles_cartesian[element_name] = build_profiles_cartesian([atom for atom in atoms if atom.type in config.get_atom_type_ids(elements)], config, header, element_name)
        if file_counter == 1:
            profiles_cartesian_avg = copy.deepcopy(profiles_cartesian)
        else:
            for group_name, profile_group in profiles_cartesian.items():
                for profile_name, profile in profile_group.items():
                    profiles_cartesian_avg[group_name][profile_name].data = update_avg_profile(profiles_cartesian_avg[group_name][profile_name].data, profile.data, file_counter)

    if config.enable_cylindrical_profiles:
        print("Building cylindrical profiles...")
        for element_name, elements in element_sets.items():
            profiles_cylindrical[element_name] = build_profiles_cylindrical([atom for atom in atoms if atom.type in config.get_atom_type_ids(elements)], config, header, wetted_area, element_name)
        if file_counter == 1:
            profiles_cylindrical_avg = copy.deepcopy(profiles_cylindrical)
        else:
            for group_name, profile_group in profiles_cylindrical.items():
                for profile_name, profile in profile_group.items():
                    profiles_cylindrical_avg[group_name][profile_name].data = update_avg_profile(profiles_cylindrical_avg[group_name][profile_name].data, profile.data, file_counter)
    
    if config.enable_spherical_profiles:
        print("Building spherical profiles...")
        for element_name, elements in element_sets.items():
            profiles_spherical[element_name] = build_profiles_spherical([atom for atom in atoms if atom.type in config.get_atom_type_ids(elements)], config, droplet_com, element_name)
        if file_counter == 1:
            profiles_spherical_avg = copy.deepcopy(profiles_spherical)
        else:
            for group_name, profile_group in profiles_spherical.items():
                for profile_name, profile in profile_group.items():
                    profiles_spherical_avg[group_name][profile_name].data = update_avg_profile(profiles_spherical_avg[group_name][profile_name].data, profile.data, file_counter)
    
    print(f"Done processing data file {os.path.basename(data_file)}")

print("Writing output files...")
summary = ""
summary += tp.print_title(config)
summary += tp.print_header(header)
if config.enable_atom_extremes: summary += tp.print_atom_extremes(atom_extremes_overall)
summary += tp.print_check_atoms_count(header, atoms)
if config.enable_atom_extremes: summary += tp.print_check_atom_extremes(header, atom_extremes_overall)
if config.enable_cartesian_profiles: summary += tp.print_check_cartesian_profiles(header, profiles_cartesian_avg["all_element"])
if config.enable_salt_concentration: summary += tp.print_salt_concentration(salt_concentration_avg)
if config.enable_vapor_count: summary += tp.print_vapor_count(vapor_count_avg)
if config.enable_droplet_com: summary += tp.print_droplet_center(droplet_com_avg)
summary += tp.print_files_used(config.data_files)

file_writer.write_summary(summary)
if config.enable_cartesian_profiles: file_writer.write_profile_group("cartesian", profiles_cartesian_avg)
if config.enable_cylindrical_profiles: file_writer.write_profile_group("cylindrical", profiles_cylindrical_avg)
if config.enable_spherical_profiles: file_writer.write_profile_group("spherical", profiles_spherical_avg)

print("ANALYSIS COMPLETE")