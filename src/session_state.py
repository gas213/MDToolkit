import logging
import os.path
import sys

from md_dataclasses.atom import Atom
from md_dataclasses.header import Header
from md_dataclasses.vector3d import Vector3D
from md_filters.filter_interface import Filter

_formatter = logging.Formatter("%(asctime)s - %(message)s")

class SessionState:
    logger: logging.Logger = logging.getLogger("main")
    step_start: int = None
    step_end: int = None
    data_path: str = None
    results_path: str = None
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

    def __init__(self):
        self.logger.setLevel(logging.DEBUG)
        self.logger.form="%(asctime)s [%(levelname)s] %(message)s"
        self.logger.handlers = [
            logging.StreamHandler(sys.stdout)
        ]

    def set_results_path(self, results_path):
        self.results_path = results_path
        file_handler = logging.FileHandler(os.path.join(results_path, "log.txt"))
        file_handler.setFormatter(_formatter)
        self.logger.handlers = [
            logging.StreamHandler(sys.stdout),
            file_handler,
        ]