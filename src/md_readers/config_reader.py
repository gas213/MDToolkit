import configparser
import os.path

from constants import masses

class ConfigReader:
    def __init__(self, config_path: str):
        self.config = configparser.ConfigParser()
        if not os.path.isfile(config_path): raise Exception(f"Config file not found at path: {config_path}")
        self.config.read(config_path)
        self._data_path = self.config["DEFAULT"]["DataPath"]
        self._data_type = self.config["DEFAULT"]["DataType"]
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

    @property
    def data_path(self) -> str:
        return self._data_path
    
    @property
    def data_type(self) -> str:
        return self._data_type
    
    @property
    def data_columns(self) -> dict[str, int]:
        return self._data_columns
    
    @property
    def approx_sphere(self) -> dict[str, float]:
        return self._approx_sphere
    
    @property
    def mass_lookup(self) -> dict[int, float]:
        return self._mass_lookup
    
    def get_atom_type_ids(self, elements: list[str]) -> list[int]:
        type_ids = []
        for element in elements:
            if element not in self._atom_types.values():
                raise Exception(f"Element not found in config: {element}")
        for key, value in self._atom_types.items():
            if value in elements:
                type_ids.append(key)
        return type_ids