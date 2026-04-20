import os.path

from md_domain.analysis import Analysis
from md_domain.atom import Atom
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
        self.data_files: dict[int, str] = {}
        self.step_current: int = 0
        self.is_finished: bool = False
        self.data_file_type: DataFileType | None = None
        self.atom_data_columns: dict[AtomDataColumnType, int] = {}
        self.atom_masses: dict[int, float] = {}
        self.header: Header | None = None
        self.atoms: list[Atom] = []
        self.analyses: dict[str, Analysis] = {}
        self.center_of_mass: Vector3D | None = None
        self.filters: dict[str, Filter] = {}

    def set_results_path(self, results_path):
        self.results_path = results_path
        self.md_logger.set_file_handler(results_path)

    def get_data_file_index(self) -> int:
        return list(self.data_files).index(self.step_current)

    def get_filtered_atoms(self, filter_name: str) -> list[Atom]:
        if filter_name.lower() == "all":
            return self.atoms
        elif filter_name in self.filters:
            return self.filters[filter_name].apply(self.atoms)
        else:
            raise Exception(f"Filter name not found: {filter_name}")
        
    def write_analyses_files(self):
        if self.results_path is None or not os.path.isdir(self.results_path):
            raise Exception("Cannot write analysis files before results path has been set.")
        for path_relative, analysis in self.analyses.items():
            write_path_full: str = os.path.join(str(self.results_path), path_relative)
            os.makedirs(os.path.dirname(write_path_full), exist_ok=True)
            with open(write_path_full, "w") as file:
                file.write(analysis.get_printable())