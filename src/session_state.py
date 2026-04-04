from md_domain.atom import Atom
from md_domain.header import Header
from md_domain.salt_histogram import SaltHistogram
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
        self.data_files_index: int = 0
        self.data_file_type: DataFileType | None = None
        self.atom_data_columns: dict[AtomDataColumnType, int] = {}
        self.atom_masses: dict[int, float] = {}
        self.header: Header | None = None
        self.atoms: list[Atom] = []
        self.center_of_mass: Vector3D | None = None
        self.filters: dict[str, Filter] = {}
        self.radial_profile: dict[float, float] = {} # TODO: this is a workaround
        self.histogram_na_centric: SaltHistogram | None = None # TODO: this is a workaround
        self.histogram_cl_centric: SaltHistogram | None = None # TODO: this is a workaround

    def set_results_path(self, results_path):
        self.results_path = results_path
        self.md_logger.set_file_handler(results_path)

    def get_filtered_atoms(self, filter_name: str) -> list[Atom]:
        if filter_name.lower() == "all":
            return self.atoms
        elif filter_name in self.filters:
            return self.filters[filter_name].apply(self.atoms)
        else:
            raise Exception(f"Filter name not found: {filter_name}")