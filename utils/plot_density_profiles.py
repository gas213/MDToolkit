# Plot radial density profiles for paper
import csv
from dataclasses import dataclass
from enum import Enum
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
from matplotlib.transforms import ScaledTranslation
import os.path

CSV_PATH: str = "/home/greg/Downloads/DensityProfileFigureData.csv"
FIG_WIDTH: int = 24 # Total width of entire figure image, in inches
FIG_HEIGHT: int = 18 # Total height of entire figure image, in inches
DEFAULT_FONT_FAMILY: str = "serif" # Default font family for all text in the figure
DEFAULT_SERIF_FONT: str = "cmr10" # Specific serif font to use for all text in the figure (cmr10 == Computer Modern Roman, the default LaTeX font)
DEFAULT_FONT_SIZE: float = 24 # Default font size for all text in the figure, in points
SUBPLOT_PADDING_X: float = 0.2 # Extra horizontal whitespace between subplots, in inches
SUBPLOT_PADDING_Y: float = 0.5 # Extra vertical whitespace between subplots, in inches
SUBPLOT_LETTER_OFFSET_X: float = -1.0 # Horizontal offset for subplot letter labels
SUBPLOT_LETTER_OFFSET_Y: float = 0.5 # Vertical offset for subplot letter labels
X_TICKS: list[int] = [15, 35, 55, 75, 95, 115]
Y_TICKS: list[float] = [0.0, 0.5, 1.0, 1.5]
YLIM_MAX: float = 1.75

class TimePeriod(Enum):
    EARLY = "Early"
    MID = "Mid"
    LATE = "Late"

class Substance(Enum):
    NACL = "NaCl"
    H2O = "H2O"

@dataclass
class Profile:
    concentration: int
    temperature: int
    time_period: TimePeriod
    substance: Substance
    data: list[float]

def build_subplot(all_profiles: list[Profile], temperature: int, time: TimePeriod, ax: Axes) -> None:
    profile_group: list[Profile] = [profile for profile in all_profiles if profile.temperature == temperature and profile.time_period == time]
    for concentration in [8, 16, 24]:
        for substance in [Substance.NACL, Substance.H2O]:
            profile = next(profile for profile in profile_group if profile.concentration == concentration and profile.substance == substance)
            line_color: str = "black" if concentration == 8 else "red" if concentration == 16 else "blue"
            line_style: str = "-" if substance == Substance.NACL else "--"
            ax.plot(r_values, profile.data, label=f"{concentration}% {substance.value}", color=line_color, linestyle=line_style)
    ax.set_xlabel("Radius (Angstroms)")
    ax.set_xticks(X_TICKS)
    ax.set_xlim(X_TICKS[0], X_TICKS[-1])
    ax.set_ylabel("Normalized Density")
    ax.set_ylim(0, YLIM_MAX)
    ax.set_yticks(Y_TICKS)

profiles: list[Profile] = []
for time in [TimePeriod.EARLY, TimePeriod.MID, TimePeriod.LATE]:
    for temperature in [25, 80]:
        for concentration in [8, 16, 24]:
            for substance in [Substance.NACL, Substance.H2O]:
                profiles.append(Profile(concentration, temperature, time, substance, []))

r_values: list[float] = []
with open(CSV_PATH, "r") as csv_file:
    reader = csv.reader(csv_file)
    next(reader)  # Skip header row
    for row in reader:
        r_values.append(float(row[0]))
        for i in range (1, len(row)):
            profiles[i - 1].data.append(float(row[i]))

plt.rc("font", family=DEFAULT_FONT_FAMILY, serif=DEFAULT_SERIF_FONT, size=DEFAULT_FONT_SIZE)
fig, axes = plt.subplots(3, 2, figsize=(FIG_WIDTH, FIG_HEIGHT), gridspec_kw={'hspace': SUBPLOT_PADDING_Y, 'wspace': SUBPLOT_PADDING_X})
build_subplot(profiles, 25, TimePeriod.EARLY, axes[0, 0])
build_subplot(profiles, 80, TimePeriod.EARLY, axes[0, 1])
build_subplot(profiles, 25, TimePeriod.MID, axes[1, 0])
build_subplot(profiles, 80, TimePeriod.MID, axes[1, 1])
build_subplot(profiles, 25, TimePeriod.LATE, axes[2, 0])
build_subplot(profiles, 80, TimePeriod.LATE, axes[2, 1])

letters = ["a)", "b)", "c)", "d)", "e)", "f)"]
for i, ax in enumerate(axes.flat):
    offset = ScaledTranslation(SUBPLOT_LETTER_OFFSET_X, SUBPLOT_LETTER_OFFSET_Y, fig.dpi_scale_trans)
    ax.text(0.0, 1.0, letters[i], transform=ax.transAxes + offset)

plt.savefig(os.path.splitext(CSV_PATH)[0] + ".png")