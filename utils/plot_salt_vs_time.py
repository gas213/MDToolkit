# Plot "salt vs. time" profiles given a directory of .txt files containing pairs of time steps and NaCl counts.
import matplotlib.pyplot as plt
import os

DATA_DIR: str = ""
DEFAULT_FONT_FAMILY: str = "serif" # Default font family for all text in the figure
DEFAULT_SERIF_FONT: str = "cmr10" # Specific serif font to use for all text in the figure (cmr10 == Computer Modern Roman, the default LaTeX font)
DEFAULT_FONT_SIZE: float = 24 # Default font size for all text in the figure, in points
FIG_WIDTH: int = 12 # Total width of entire figure image, in inches
FIG_HEIGHT: int = 9 # Total height of entire figure image, in inches
TIME_CONVERSION_FACTOR: float = 2e-6 # Conversion factor from time steps to nanoseconds (assuming 2 fs per time step)
X_TICKS: list[float] = [0, 1.0, 2.0, 3.0, 4.0]

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
plt.subplots(constrained_layout=True, figsize=(FIG_WIDTH, FIG_HEIGHT)) # Fix for axis labels getting cut off at the bottom of the saved image
plt.plot([t * TIME_CONVERSION_FACTOR for t in data.keys()], list(data.values()))
plt.title("Na + Cl Atom Count vs. Time")
plt.xlabel("Time (ns)")
plt.ylabel("Na + Cl Atom Count")
plt.xlim(list(data.keys())[0] * TIME_CONVERSION_FACTOR, list(data.keys())[-1] * TIME_CONVERSION_FACTOR)
plt.xticks(X_TICKS)

plt.savefig(os.path.join(DATA_DIR, "salt_vs_time.png"))