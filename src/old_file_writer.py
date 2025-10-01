import os.path

from old_constants import element_sets
from md_dataclasses.density_profile import DensityProfile
from md_readers.config_reader import ConfigReader
import old_text_printer as tp

"""
FULL FILE STRUCTURE:

{dir containing 123.data}/
    analysis/
        123/
            profiles/
                cartesian/
                    {element}/
                        {profile}.txt
                spherical/
                    {element}/
                        {profile}.txt
            summary.txt
"""

class FileWriter:
    DIR_ANALYSIS: str = "analysis"
    DIR_PROFILES: str = "profiles"

    _path_analysis: str = None
    _path_results: str = None

    def __init__(self, config: ConfigReader):
        self._config = config

    def mkdir_analysis(self) -> None:
        path_source = os.path.dirname(self._config.data_path)
        self._path_analysis = os.path.join(path_source, self.DIR_ANALYSIS)
        if not os.path.isdir(self._path_analysis): os.makedirs(self._path_analysis)

    def mkdir_results(self) -> None:
        if self._path_analysis is None: self.mkdir_analysis(self._config)

        if self._config.is_multi_file:
            prefix = os.path.basename(self._config.data_path).split("*")[0]
            self._path_results = os.path.join(self._path_analysis, f"{prefix}{self._config.step_start}_{self._config.step_end}")
        else:
            self._path_results = os.path.join(self._path_analysis, str.split(os.path.basename(self._config.data_path), ".")[0])

        if os.path.isdir(self._path_results):
            raise Exception(f"Directory already exists: {self._path_results}")
        else:
            os.makedirs(self._path_results)

    def mkdirs_initial(self) -> None:
        self.mkdir_analysis()
        self.mkdir_results()

    def mkdir_profiles(self) -> str:
        if self._path_results is None: self.mkdir_results(self._config)
        
        path_profiles = os.path.join(self._path_results, self.DIR_PROFILES)
        if not os.path.isdir(path_profiles): os.makedirs(path_profiles)
        return path_profiles

    def write_profile_group(self, name: str, profiles: dict[str, dict[str, DensityProfile]]) -> None:
        path_profile_group = os.path.join(self.mkdir_profiles(), name)
        os.makedirs(path_profile_group)
        for element_name in element_sets.keys():
            path_element = os.path.join(path_profile_group, element_name)
            os.makedirs(path_element)
            for profile_name, profile in profiles[element_name].items():
                with open(os.path.join(path_element, f"{profile_name}.txt"), "w") as out: out.write(tp.print_density_profile(profile))

    def write_summary(self, summary: str) -> None:
        if self._path_results is None: self.mkdir_results()
        with open(os.path.join(self._path_results, "summary.txt"), "w") as out: out.write(summary)