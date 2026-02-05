from md_dataclasses.atom import Atom
from md_dataclasses.header import Header
from md_dataclasses.vector3d import Vector3D
from md_filters.filter_interface import Filter

class SessionState:
    step_start: int = None
    step_end: int = None
    data_path: str = None
    data_files: list[str] = []
    data_files_index: int = 0
    data_type: str = None
    atom_data_columns: dict[str, int] = {}
    atom_masses: dict[int, float] = {}
    header: Header = None
    atoms: list[Atom] = []
    center_of_mass: Vector3D = None
    filters: dict[str, Filter] = {}
    radial_profile: dict[float, float] = {} # TODO: this is a workaround