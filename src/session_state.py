import glob
import os.path

from md_domain.analysis import Analysis
from md_domain.atom import Atom
from md_domain.center_of_mass import CenterOfMass
from md_domain.header import Header
from md_domain.vector3d import Vector3D
from md_enums.atom_data_column_type import AtomDataColumnType
from md_enums.data_file_type import DataFileType
from md_filters.filter_interface import Filter
from md_logger import MDLogger

class SessionState:
    def __init__(self):
        self.md_logger = MDLogger()
        self.step_start: int | None = None
        self.step_end: int | None = None
        self.data_path: str | None = None
        self.results_path: str | None = None
        self.data_filenames: dict[int, str] = {}
        self.step_current: int = 0
        self.is_finished: bool = False
        self.data_file_type: DataFileType | None = None
        self.atom_data_columns: dict[AtomDataColumnType, int] = {}
        self.atom_masses: dict[int, float] = {}
        self.header: Header | None = None
        self.atoms: list[Atom] = []
        self.analyses: dict[str, Analysis] = {}
        self.filters: dict[str, Filter] = {}

    def new_paths(self, data_path: str, results_path: str | None = None):
        self.data_path = data_path
        self.make_results_path(results_path)
        self.load_data_filenames()
        self.step_current = list(self.data_filenames.keys())[0]

    def load_data_filenames(self):
        if self.data_path is None:
            raise Exception("data_path must be set before loading data filenames.")
        self.data_filenames.clear()
        filename_stripped = os.path.splitext(os.path.basename(self.data_path))[0]
        if ("*" in filename_stripped):
            if self.step_start is None:
                raise Exception("Missing value for step_start")
            elif self.step_end is None:
                raise Exception("Missing value for step_end")
            elif filename_stripped.count("*") > 1:
                raise Exception("Cannot have multiple wildcards (*) in data_path value")
            elif self.step_start > self.step_end:
                raise Exception("Value of step_start must be less than or equal to step_end")
            path_before_wildcard = self.data_path.split("*")[0]
            path_after_wildcard = self.data_path.split("*")[1]
            wildcard_matches = glob.glob(self.data_path)
            valid_step_numbers: list[int] = []
            # Order data files by step number
            for match in wildcard_matches:
                step_str = match.replace(path_before_wildcard, "").replace(path_after_wildcard, "")
                if step_str.isdigit() and int(step_str) >= self.step_start and int(step_str) <= self.step_end:
                    valid_step_numbers.append(int(step_str))
            valid_step_numbers.sort()
            if len(valid_step_numbers) == 0:
                raise Exception(f"No data files were found matching the specified pattern of {self.data_path} while having a step number in the range of {self.step_start} through {self.step_end}")
            for step in valid_step_numbers:
                self.data_filenames[step] = path_before_wildcard + str(step) + path_after_wildcard
        elif not os.path.isfile(self.data_path):
            raise Exception(f"No data file was found at the specified path: {self.data_path}")        
        else:
            # If only loading a single data/dump file, just assign it a step number of 0
            self.data_filenames[0] = self.data_path

    def make_results_path(self, results_path: str | None):
        if self.data_path is None:
            raise Exception("data_path must be set before making results directory.")
        root_path = os.path.dirname(self.data_path)

        if results_path is not None:
            self.results_path = os.path.join(root_path, results_path)
        elif self.step_start is not None and self.step_end is not None and self.step_start != self.step_end:
            prefix = os.path.basename(self.data_path).split("*")[0]
            self.results_path = os.path.join(root_path, f"{prefix}{self.step_start}_{self.step_end}")
        else:
            self.results_path = os.path.join(root_path, str.split(os.path.basename(self.data_path), ".")[0])

        if os.path.isdir(self.results_path):
            raise Exception(f"Directory already exists: {self.results_path}")
        else:
            os.makedirs(self.results_path)

        self.md_logger.set_file_handler(self.results_path)

    def get_data_file_index(self) -> int:
        return list(self.data_filenames).index(self.step_current)

    def get_filtered_atoms(self, filter_name: str) -> list[Atom]:
        if filter_name.lower() == "all":
            return self.atoms
        elif filter_name in self.filters:
            return self.filters[filter_name].apply(self.atoms)
        else:
            raise Exception(f"Filter name not found: {filter_name}")
        
    def get_current_com(self, com_path: str) -> Vector3D:
        if com_path not in self.analyses:
            raise Exception(f"Center of mass path '{com_path}' not found in analyses.")
        com_analysis = self.analyses[com_path]
        if not isinstance(com_analysis, CenterOfMass):
            raise Exception(f"Analysis with name '{com_path}' is not a CenterOfMass, cannot be used as center of mass.")
        if self.step_current not in com_analysis.data:
            raise Exception(f"Center of mass analysis '{com_path}' does not contain data for current step {self.step_current}.")
        return com_analysis.data[self.step_current]
        
    def write_analyses_files(self):
        if self.results_path is None or not os.path.isdir(self.results_path):
            raise Exception("Cannot write analysis files before results path has been set.")
        for path_relative, analysis in self.analyses.items():
            write_path_base: str = os.path.join(str(self.results_path), path_relative)
            os.makedirs(os.path.dirname(write_path_base), exist_ok=True)
            for suffix, printable in analysis.get_printables().items():
                write_path_full = write_path_base + "_" + suffix + ".txt"
                with open(write_path_full, "w") as file:
                    file.write(printable)