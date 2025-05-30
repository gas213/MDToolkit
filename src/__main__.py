import os.path
import sys

from md_analyses.atom_extremes import find_atom_extremes
from md_analyses.center_of_mass import calc_droplet_center
from md_analyses.density_profiles import build_density_profiles
from md_analyses.salt_concentration import calc_salt_concentration
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

overall_atom_extremes: Box = None
avg_salt_concentration: float = 0.0
avg_vapor_count: float = 0.0
avg_droplet_com: Vector3D = None
avg_density_profiles: dict[str, dict[str, DensityProfile]] = None

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

    print("Building density profiles...")
    density_profiles: dict[str, dict[str, DensityProfile]] = {
        # Individual elements
        "carbon": build_density_profiles(config, header, atoms, droplet_com, config.get_atom_type_ids(["C"]), "carbon"),
        "chlorine": build_density_profiles(config, header, atoms, droplet_com, config.get_atom_type_ids(["Cl"]), "chlorine"),
        "fluorine": build_density_profiles(config, header, atoms, droplet_com, config.get_atom_type_ids(["F"]), "fluorine"),
        "hydrogen": build_density_profiles(config, header, atoms, droplet_com, config.get_atom_type_ids(["H"]), "hydrogen"),
        "oxygen": build_density_profiles(config, header, atoms, droplet_com, config.get_atom_type_ids(["O"]), "oxygen"),
        "sodium": build_density_profiles(config, header, atoms, droplet_com, config.get_atom_type_ids(["Na"]), "sodium"),
        # Groups of elements
        "all": build_density_profiles(config, header, atoms, droplet_com, [0], "all-element"),
        "ptfe": build_density_profiles(config, header, atoms, droplet_com, config.get_atom_type_ids(["C", "F"]), "ptfe"),
        "salt": build_density_profiles(config, header, atoms, droplet_com, config.get_atom_type_ids(["Cl", "Na"]), "salt"),
        "saltwater": build_density_profiles(config, header, atoms, droplet_com, config.get_atom_type_ids(["Cl", "Na", "H", "O"]), "saltwater"),
        "water": build_density_profiles(config, header, atoms, droplet_com, config.get_atom_type_ids(["H", "O"]), "water"),
    }

    if file_counter == 1:
        overall_atom_extremes = atom_extremes
        avg_salt_concentration = salt_concentration
        avg_vapor_count = vapor_count
        avg_droplet_com = droplet_com
        avg_density_profiles = density_profiles
    elif file_counter > 1:
        division_factor = 1.0 / float(file_counter)
        if atom_extremes.lo.x < overall_atom_extremes.lo.x: overall_atom_extremes.lo.x = atom_extremes.lo.x
        if atom_extremes.hi.x > overall_atom_extremes.hi.x: overall_atom_extremes.hi.x = atom_extremes.hi.x
        if atom_extremes.lo.y < overall_atom_extremes.lo.y: overall_atom_extremes.lo.y = atom_extremes.lo.y
        if atom_extremes.hi.y > overall_atom_extremes.hi.y: overall_atom_extremes.hi.y = atom_extremes.hi.y
        if atom_extremes.lo.z < overall_atom_extremes.lo.z: overall_atom_extremes.lo.z = atom_extremes.lo.z
        if atom_extremes.hi.z > overall_atom_extremes.hi.z: overall_atom_extremes.hi.z = atom_extremes.hi.z
        avg_salt_concentration = (avg_salt_concentration * (file_counter - 1) + salt_concentration) * division_factor
        avg_vapor_count = (avg_vapor_count * (file_counter - 1) + vapor_count) * division_factor
        avg_droplet_com.x = (avg_droplet_com.x * (file_counter - 1) + droplet_com.x) * division_factor
        avg_droplet_com.y = (avg_droplet_com.y * (file_counter - 1) + droplet_com.y) * division_factor
        avg_droplet_com.z = (avg_droplet_com.z * (file_counter - 1) + droplet_com.z) * division_factor
        for group_name, profile_group in density_profiles.items():
            for profile_name, profile in profile_group.items():
                for location, count in profile.data.items():
                    avg_density_profiles[group_name][profile_name].data[location] = (avg_density_profiles[group_name][profile_name].data[location] * (file_counter - 1) + density_profiles[group_name][profile_name].data[location]) * division_factor
    
    print(f"Done processing data file {os.path.basename(data_file)}")

print("Writing output files...")
summary = ""
summary += printer.print_title(config)
summary += printer.print_header(header)
summary += printer.print_atom_extremes(overall_atom_extremes)
summary += printer.print_sanity_checks(header, overall_atom_extremes, atoms, density_profiles["all"])
summary += printer.print_salt_concentration(avg_salt_concentration)
summary += printer.print_vapor_count(avg_vapor_count)
summary += printer.print_droplet_center(avg_droplet_com)
summary += printer.print_files_used(config.data_files)
with open(os.path.join(config.dir_results, "summary.txt"), "w") as analysis: analysis.write(summary)

for group_name, profile_group in avg_density_profiles.items():
    dir_group = os.path.join(config.dir_results, f"profiles/{group_name}")
    os.makedirs(dir_group)
    for profile_name, profile in profile_group.items():
        with open(os.path.join(dir_group, f"{profile_name}.txt"), "w") as out_file: out_file.write(printer.print_density_profile(profile))

print("ANALYSIS COMPLETE")