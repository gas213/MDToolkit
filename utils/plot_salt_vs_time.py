# Plot "salt vs. time" profiles given a directory of .txt files containing pairs of time steps and NaCl counts.
import matplotlib.pyplot as plt
import os

DATA_DIR: str = ""
DEFAULT_FONT_FAMILY: str = "serif" # Default font family for all text in the figure
DEFAULT_SERIF_FONT: str = "cmr10" # Specific serif font to use for all text in the figure (cmr10 == Computer Modern Roman, the default LaTeX font)
DEFAULT_FONT_SIZE: float = 24 # Default font size for all text in the figure, in points

data: dict[int, int] = {}
for entry in os.scandir(DATA_DIR):
    if entry.is_file() and entry.name.endswith(".txt"):
        with open(entry.path, "r") as file:
            for line in file:
                time_step, nacl_count = line.strip().split()
                if time_step in data:
                    raise ValueError(f"Duplicate time step {time_step} found while reading {entry.name}")
                data[int(time_step)] = int(nacl_count)
data = dict(sorted(data.items()))

plt.rc("font", family=DEFAULT_FONT_FAMILY, serif=DEFAULT_SERIF_FONT, size=DEFAULT_FONT_SIZE)
plt.plot(list(data.keys()), list(data.values()))
plt.title("NaCl Count vs. Time Step")
plt.xlabel("Time Step")
plt.ylabel("NaCl Count")

plt.savefig(os.path.join(DATA_DIR, "salt_vs_time.png"))