from md_dataclasses.atom import Atom
from md_dataclasses.header import Header
from md_dataclasses.vector3d import Vector3D
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
        self.data_files: list[str] = []
        self.data_files_index: int = 0
        self.data_file_type: DataFileType | None = None
        self.atom_data_columns: dict[AtomDataColumnType, int] = {}
        self.atom_masses: dict[int, float] = {}
        self.header: Header | None = None
        self.atoms: list[Atom] = []
        self.center_of_mass: Vector3D | None = None
        self.filters: dict[str, Filter] = {}
        self.radial_profile: dict[float, float] = {} # TODO: this is a workaround
        self.cl_neighbors_histogram: dict[int, float] = {} # TODO: this is a workaround
        self.na_neighbors_histogram: dict[int, float] = {} # TODO: this is a workaround

    def set_results_path(self, results_path):
        self.results_path = results_path
        self.md_logger.set_file_handler(results_path)