from dataclasses import dataclass

from md_dataclasses.box import Box

@dataclass
class Header:
    atom_count: int
    box: Box

    def __str__(self):
        return f"Atom count: {self.atom_count}\nBox: {self.box}"