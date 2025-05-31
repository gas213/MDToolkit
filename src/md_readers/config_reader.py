import configparser
import glob
import os.path

from constants import masses

class ConfigReader:
    def __init__(self, config_path: str):
        self.config = configparser.ConfigParser()
        if not os.path.isfile(config_path): raise Exception(f"Config file not found at path: {config_path}")
        self.config.read(config_path)
        self._is_multi_file = False
        self._data_path = self.config["DEFAULT"]["DataPath"]
        self._step_start = self.config["DEFAULT"]["StepStart"]
        self._step_end = self.config["DEFAULT"]["StepEnd"]
        self._data_type = self.config["DEFAULT"]["DataType"]
        self._cartesian_profile_step_xyz = float(self.config["DEFAULT"]["CartesianProfileStepXYZ"])
        self._spherical_profile_step_r = float(self.config["DEFAULT"]["SphericalProfileStepR"])
        self._spherical_profile_start_r = float(self.config["DEFAULT"]["SphericalProfileStartR"])
        if self._data_type == "NetCDF":
            self._data_columns = {}
        else:
            self._data_columns = {
                "Id": int(self.config[self._data_type]["ColumnAtomId"]),
                "Type": int(self.config[self._data_type]["ColumnAtomType"]),
                "X": int(self.config[self._data_type]["ColumnAtomX"]),
                "Y": int(self.config[self._data_type]["ColumnAtomY"]),
                "Z": int(self.config[self._data_type]["ColumnAtomZ"]),
            }
        self._approx_sphere = {
            "X": float(self.config["DEFAULT"]["ApproxSphereX"]),
            "Y": float(self.config["DEFAULT"]["ApproxSphereY"]),
            "Z": float(self.config["DEFAULT"]["ApproxSphereZ"]),
            "R": float(self.config["DEFAULT"]["ApproxSphereR"]),
        }
        atom_type_set = self.config["DEFAULT"]["AtomTypeSet"]
        self._atom_types = {
            int(self.config[atom_type_set]["AtomTypeC1"]): "C",
            int(self.config[atom_type_set]["AtomTypeC2"]): "C",
            int(self.config[atom_type_set]["AtomTypeCl"]): "Cl",
            int(self.config[atom_type_set]["AtomTypeF"]): "F",
            int(self.config[atom_type_set]["AtomTypeH"]): "H",
            int(self.config[atom_type_set]["AtomTypeNa"]): "Na",
            int(self.config[atom_type_set]["AtomTypeO"]): "O",
        }
        self._mass_lookup = {}
        for key, value in self._atom_types.items():
            self._mass_lookup[key] = masses[value]
        self.set_data_files()
        self.make_directories()

    @property
    def data_path(self) -> str:
        return self._data_path
    
    @property
    def step_start(self) -> str:
        return self._step_start
    
    @property
    def step_end(self) -> str:
        return self._step_end
    
    @property
    def data_type(self) -> str:
        return self._data_type
    
    @property
    def cartesian_profile_step_xyz(self) -> float:
        return self._cartesian_profile_step_xyz
    
    @property
    def spherical_profile_step_r(self) -> float:
        return self._spherical_profile_step_r

    @property
    def spherical_profile_start_r(self) -> float:
        return self._spherical_profile_start_r
    
    @property
    def data_columns(self) -> dict[str, int]:
        return self._data_columns
    
    @property
    def approx_sphere(self) -> dict[str, float]:
        return self._approx_sphere
    
    @property
    def mass_lookup(self) -> dict[int, float]:
        return self._mass_lookup
    
    @property
    def data_files(self) -> list[str]:
        return self._data_files
    
    @property
    def dir_results(self) -> str:
        return self._dir_results
    
    def get_atom_type_ids(self, elements: list[str]) -> list[int]:
        type_ids = []
        for element in elements:
            if element not in self._atom_types.values():
                raise Exception(f"Element not found in config: {element}")
        for key, value in self._atom_types.items():
            if value in elements:
                type_ids.append(key)
        return type_ids
    
    def set_data_files(self):
        if self._data_path is None:
            raise Exception("Data file path not provided")
        
        filename_stripped = os.path.splitext(os.path.basename(self._data_path))[0]
        if ("*" in filename_stripped):
            self._is_multi_file = True
            if filename_stripped.count("*") > 1:
                raise Exception("Cannot have multiple wildcards (*) in the config DataPath")
            elif not self._step_start.isdigit() or not self._step_end.isdigit():
                raise Exception("Config values for StepStart and StepEnd must be integers")
            elif int(self._step_start) > int(self._step_end):
                raise Exception("Config value StepStart must be less than or equal to StepEnd")
        elif not os.path.isfile(self._data_path):
            raise Exception(f"No data file was found at the specified path: {self._data_path}")

        self._data_files = []
        if self._is_multi_file:
            path_before_wildcard = self._data_path.split("*")[0]
            path_after_wildcard = self._data_path.split("*")[1]
            step_start = int(self._step_start)
            step_end = int(self._step_end)
            wildcard_matches = glob.glob(self._data_path)
            for match in wildcard_matches:
                step_str = match.replace(path_before_wildcard, "").replace(path_after_wildcard, "")
                if step_str.isdigit() and int(step_str) >= step_start and int(step_str) <= step_end:
                    self._data_files.append(match)
        else:
            self._data_files.append(self._data_path)

        return
    
    def make_directories(self):
        """
        Creates folder structure for outputting results.\n
        Example for file named 123.data:\n
        - {directory containing 123.data}/
        \t- analysis/
        \t\t- 123/
        \t\t\t- profiles/
        """

        dir_root = os.path.dirname(self._data_path)
        dir_analysis = os.path.join(dir_root, "analysis")
        if not os.path.isdir(dir_analysis): os.makedirs(dir_analysis)

        if self._is_multi_file:
            prefix = os.path.basename(self._data_path).split("*")[0]
            self._dir_results = os.path.join(dir_analysis, f"{prefix}{self._step_start}_{self._step_end}")
        else:
            self._dir_results = os.path.join(dir_analysis, str.split(os.path.basename(self._data_path), ".")[0])

        dir_profiles = os.path.join(self._dir_results, "profiles")
        if os.path.isdir(self._dir_results):
            raise Exception(f"Directory already exists: {self._dir_results}")
        else:
            os.makedirs(self._dir_results)
            os.makedirs(dir_profiles)

        return