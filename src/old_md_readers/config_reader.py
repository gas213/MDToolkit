import configparser
import glob
import os.path

from old_constants import masses

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
        self._enable_atom_extremes = self.config["DEFAULT"].getboolean("EnableAtomExtremes")
        self._enable_salt_concentration = self.config["DEFAULT"].getboolean("EnableSaltConcentration")
        self._enable_vapor_count = self.config["DEFAULT"].getboolean("EnableVaporCount")
        self._enable_droplet_com = self.config["DEFAULT"].getboolean("EnableDropletCOM")
        self._enable_cartesian_profiles = self.config["DEFAULT"].getboolean("EnableCartesianProfiles")
        self._enable_cylindrical_profiles = self.config["DEFAULT"].getboolean("EnableCylindricalProfiles")
        self._enable_spherical_profiles = self.config["DEFAULT"].getboolean("EnableSphericalProfiles")
        self._enable_wetted_area = self.config["DEFAULT"].getboolean("EnableWettedArea")
        self._vapor_threshold = self.config["DEFAULT"].getfloat("VaporThreshold")
        self._wetting_threshold = self.config["DEFAULT"].getfloat("WettingThreshold")
        self._cartesian_profile_step_xyz = self.config["DEFAULT"].getfloat("CartesianProfileStepXYZ")
        self._cylindrical_profile_start_r = self.config["DEFAULT"].getfloat("CylindricalProfileStartR")
        self._cylindrical_profile_step_r = self.config["DEFAULT"].getfloat("CylindricalProfileStepR")
        self._cylindrical_profile_step_z = self.config["DEFAULT"].getfloat("CylindricalProfileStepZ")
        self._spherical_profile_step_r = self.config["DEFAULT"].getfloat("SphericalProfileStepR")
        self._spherical_profile_start_r = self.config["DEFAULT"].getfloat("SphericalProfileStartR")
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
            "C": [int(self.config[atom_type_set]["AtomTypeC1"]), int(self.config[atom_type_set]["AtomTypeC2"])],
            "Cl": [int(self.config[atom_type_set]["AtomTypeCl"])],
            "F": [int(self.config[atom_type_set]["AtomTypeF"])],
            "H": [int(self.config[atom_type_set]["AtomTypeH"])],
            "Na": [int(self.config[atom_type_set]["AtomTypeNa"])],
            "O": [int(self.config[atom_type_set]["AtomTypeO"])],
        }
        self._mass_lookup = {}
        for key, value in self._atom_types.items():
            for type_id in value:
                self._mass_lookup[type_id] = masses[key]
        self.set_data_files()

    @property
    def is_multi_file(self) -> bool:
        return self._is_multi_file

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
    def enable_atom_extremes(self) -> bool:
        return self._enable_atom_extremes
    
    @property
    def enable_salt_concentration(self) -> bool:
        return self._enable_salt_concentration
    
    @property
    def enable_vapor_count(self) -> bool:
        return self._enable_vapor_count
    
    @property
    def enable_droplet_com(self) -> bool:
        return self._enable_droplet_com or self._enable_spherical_profiles
    
    @property
    def enable_cartesian_profiles(self) -> bool:
        return self._enable_cartesian_profiles

    @property
    def enable_cylindrical_profiles(self) -> bool:
        return self._enable_cylindrical_profiles
    
    @property
    def enable_spherical_profiles(self) -> bool:
        return self._enable_spherical_profiles
    
    @property
    def enable_wetted_area(self) -> bool:
        return self._enable_wetted_area or self._enable_cylindrical_profiles
    
    @property
    def vapor_threshold(self) -> float:
        return self._vapor_threshold
    
    @property
    def wetting_threshold(self) -> float:
        return self._wetting_threshold
    
    @property
    def cartesian_profile_step_xyz(self) -> float:
        return self._cartesian_profile_step_xyz
    
    @property
    def cylindrical_profile_start_r(self) -> float:
        return self._cylindrical_profile_start_r
    
    @property
    def cylindrical_profile_step_r(self) -> float:
        return self._cylindrical_profile_step_r
    
    @property
    def cylindrical_profile_step_z(self) -> float:
        return self._cylindrical_profile_step_z
    
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
    
    def get_atom_type_ids(self, elements: list[str]) -> list[int]:
        type_ids = []
        if len(elements) == 1 and (elements[0] in ["All", "all", "ALL"]):
            for key, value in self._atom_types.items():
                type_ids.extend(value)
            return type_ids
        for element in elements:
            if element not in self._atom_types.keys():
                raise Exception(f"Element not found in config: {element}")
        for key, value in self._atom_types.items():
            if key in elements:
                type_ids.extend(value)
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
            valid_step_numbers: list[int] = []
            # Order data files by step number
            for match in wildcard_matches:
                step_str = match.replace(path_before_wildcard, "").replace(path_after_wildcard, "")
                if step_str.isdigit() and int(step_str) >= step_start and int(step_str) <= step_end:
                    valid_step_numbers.append(int(step_str))
            valid_step_numbers.sort()
            for step in valid_step_numbers:
                self._data_files.append(path_before_wildcard + str(step) + path_after_wildcard)
        else:
            self._data_files.append(self._data_path)

        return