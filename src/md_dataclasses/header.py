from dataclasses import dataclass

from md_dataclasses.box import Box

@dataclass
class Header:
    atom_count: int
    box: Box