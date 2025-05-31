import os.path
import sys

from md_analyses.atom_extremes import find_atom_extremes
from md_analyses.center_of_mass import calc_droplet_center
from md_analyses.density_profiles import build_profiles_cartesian, build_profiles_spherical
from md_analyses.salt_concentration import calc_salt_concentration
from md_analyses.time_aggregator import update_atom_extremes, update_avg_scalar, update_avg_profile
from md_analyses.vapor_count import count_vapor_particles
from md_dataclasses.box import Box
from md_dataclasses.density_profile import DensityProfile
from md_dataclasses.vector3d import Vector3D
from md_readers.argv_reader import read_config_path
from md_readers.config_reader import ConfigReader
from md_readers.data_reader_mediator import read_header, read_atoms
import printer

print("Reading config and making directories...")
config = ConfigReader(read_config_path(sys.argv))
file_counter = 0
file_count = len(config.data_files)

print("Reading header of first data file...")
header = read_header(config, config.data_files[0])

atom_extremes_overall: Box = None
salt_concentration_avg: float = 0.0
vapor_count_avg: float = 0.0
droplet_com_avg: Vector3D = Vector3D(0.0, 0.0, 0.0)
profiles_cartesian_avg: dict[str, dict[str, DensityProfile]] = None
profiles_spherical_avg: dict[str, dict[str, DensityProfile]] = None

for data_file in config.data_files:
    file_counter += 1
    print(f"Begin processing data file {file_counter}/{file_count}: {os.path.basename(data_file)}")

    print("Reading atoms...")
    atoms = read_atoms(config, data_file)

    print("Finding atom extremes...")
    atom_extremes = find_atom_extremes(atoms)

    print("Calculating salt concentration...")
    salt_concentration = calc_salt_concentration(config, atoms)

    print("Counting vapor molecules...")
    vapor_count = count_vapor_particles(config, atoms)

    print("Calculating droplet center of mass...")
    droplet_com = calc_droplet_center(config, atoms)

    print("Building cartesian profiles...")
    profiles_cartesian: dict[str, dict[str, DensityProfile]] = {
        # Individual elements
        "carbon": build_profiles_cartesian([atom for atom in atoms if atom.type in config.get_atom_type_ids(["C"])], config, header, "carbon"),
        "chlorine": build_profiles_cartesian([atom for atom in atoms if atom.type in config.get_atom_type_ids(["Cl"])], config, header, "chlorine"),
        "fluorine": build_profiles_cartesian([atom for atom in atoms if atom.type in config.get_atom_type_ids(["F"])], config, header, "fluorine"),
        "hydrogen": build_profiles_cartesian([atom for atom in atoms if atom.type in config.get_atom_type_ids(["H"])], config, header, "hydrogen"),
        "oxygen": build_profiles_cartesian([atom for atom in atoms if atom.type in config.get_atom_type_ids(["O"])], config, header, "oxygen"),
        "sodium": build_profiles_cartesian([atom for atom in atoms if atom.type in config.get_atom_type_ids(["Na"])], config, header, "sodium"),
        # Groups of elements
        "all": build_profiles_cartesian(atoms, config, header, "all-element"), 
        "ptfe": build_profiles_cartesian([atom for atom in atoms if atom.type in config.get_atom_type_ids(["C", "F"])], config, header, "ptfe"),
        "salt": build_profiles_cartesian([atom for atom in atoms if atom.type in config.get_atom_type_ids(["Cl", "Na"])], config, header, "salt"),
        "saltwater": build_profiles_cartesian([atom for atom in atoms if atom.type in config.get_atom_type_ids(["Cl", "Na", "H", "O"])], config, header, "saltwater"),
        "water": build_profiles_cartesian([atom for atom in atoms if atom.type in config.get_atom_type_ids(["H", "O"])], config, header, "water"),
    }

    print("Building spherical profiles...")
    profiles_spherical: dict[str, dict[str, DensityProfile]] = {
        # Individual elements
        "carbon": build_profiles_spherical([atom for atom in atoms if atom.type in config.get_atom_type_ids(["C"])], config, droplet_com, "carbon"),
        "chlorine": build_profiles_spherical([atom for atom in atoms if atom.type in config.get_atom_type_ids(["Cl"])], config, droplet_com, "chlorine"),
        "fluorine": build_profiles_spherical([atom for atom in atoms if atom.type in config.get_atom_type_ids(["F"])], config, droplet_com, "fluorine"),
        "hydrogen": build_profiles_spherical([atom for atom in atoms if atom.type in config.get_atom_type_ids(["H"])], config, droplet_com, "hydrogen"),
        "oxygen": build_profiles_spherical([atom for atom in atoms if atom.type in config.get_atom_type_ids(["O"])], config, droplet_com, "oxygen"),
        "sodium": build_profiles_spherical([atom for atom in atoms if atom.type in config.get_atom_type_ids(["Na"])], config, droplet_com, "sodium"),
        # Groups of elements
        "all": build_profiles_spherical(atoms, config, droplet_com, "all-element"),
        "ptfe": build_profiles_spherical([atom for atom in atoms if atom.type in config.get_atom_type_ids(["C", "F"])], config, droplet_com, "ptfe"),
        "salt": build_profiles_spherical([atom for atom in atoms if atom.type in config.get_atom_type_ids(["Cl", "Na"])], config, droplet_com, "salt"),
        "saltwater": build_profiles_spherical([atom for atom in atoms if atom.type in config.get_atom_type_ids(["Cl", "Na", "H", "O"])], config, droplet_com, "saltwater"),
        "water": build_profiles_spherical([atom for atom in atoms if atom.type in config.get_atom_type_ids(["H", "O"])], config, droplet_com, "water"),
    }

    atom_extremes_overall = update_atom_extremes(atom_extremes_overall, atom_extremes)
    salt_concentration_avg = update_avg_scalar(salt_concentration_avg, salt_concentration, file_counter)
    vapor_count_avg = update_avg_scalar(vapor_count_avg, vapor_count, file_counter)
    droplet_com_avg.x = update_avg_scalar(droplet_com_avg.x, droplet_com.x, file_counter)
    droplet_com_avg.y = update_avg_scalar(droplet_com_avg.y, droplet_com.y, file_counter)
    droplet_com_avg.z = update_avg_scalar(droplet_com_avg.z, droplet_com.z, file_counter)

    if file_counter == 1:
        profiles_cartesian_avg = profiles_cartesian.copy()
        profiles_spherical_avg = profiles_spherical.copy()
    else:
        for group_name, profile_group in profiles_cartesian.items():
            for profile_name, profile in profile_group.items():
                profiles_cartesian_avg[group_name][profile_name].data = update_avg_profile(profiles_cartesian_avg[group_name][profile_name].data, profile.data, file_counter)
        for group_name, profile_group in profiles_spherical.items():
            for profile_name, profile in profile_group.items():
                profiles_spherical_avg[group_name][profile_name].data = update_avg_profile(profiles_spherical_avg[group_name][profile_name].data, profile.data, file_counter)
    
    print(f"Done processing data file {os.path.basename(data_file)}")

print("Writing output files...")
summary = ""
summary += printer.print_title(config)
summary += printer.print_header(header)
summary += printer.print_atom_extremes(atom_extremes_overall)
summary += printer.print_sanity_checks(header, atom_extremes_overall, atoms, profiles_cartesian_avg["all"])
summary += printer.print_salt_concentration(salt_concentration_avg)
summary += printer.print_vapor_count(vapor_count_avg)
summary += printer.print_droplet_center(droplet_com_avg)
summary += printer.print_files_used(config.data_files)
with open(os.path.join(config.dir_results, "summary.txt"), "w") as analysis: analysis.write(summary)

for group_name, profile_group in profiles_cartesian_avg.items():
    dir_group = os.path.join(config.dir_results, f"profiles/{group_name}")
    os.makedirs(dir_group)
    for profile_name, profile in profile_group.items():
        with open(os.path.join(dir_group, f"{profile_name}.txt"), "w") as out_file: out_file.write(printer.print_density_profile(profile))
    for profile_name, profile in profiles_spherical_avg[group_name].items():
        with open(os.path.join(dir_group, f"{profile_name}.txt"), "w") as out_file: out_file.write(printer.print_density_profile(profile))

print("ANALYSIS COMPLETE")