import os.path

from constants import element_sets
from md_dataclasses.density_profile import DensityProfile
from md_readers.config_reader import ConfigReader
import text_printer as tp

dir_profiles = "profiles"

def make_dir_profiles(config: ConfigReader) -> str:
    path_profiles = os.path.join(config.path_results, dir_profiles)
    if not os.path.isdir(path_profiles): os.makedirs(path_profiles)
    return path_profiles

def write_profile_group(config: ConfigReader, name: str, profiles: dict[str, dict[str, DensityProfile]]) -> None:
    path_profile_group = os.path.join(make_dir_profiles(config), name)
    os.makedirs(path_profile_group)
    for element_name in element_sets.keys():
        path_element = os.path.join(path_profile_group, element_name)
        os.makedirs(path_element)
        for profile_name, profile in profiles[element_name].items():
            with open(os.path.join(path_element, f"{profile_name}.txt"), "w") as out_file: out_file.write(tp.print_density_profile(profile))

def write_summary(config: ConfigReader, summary: str) -> None:
    with open(os.path.join(config.path_results, "summary.txt"), "w") as analysis: analysis.write(summary)