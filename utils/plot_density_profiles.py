# Plot radial density profiles for paper
import csv
from dataclasses import dataclass
from enum import Enum
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
from matplotlib.transforms import ScaledTranslation
import os.path

CSV_PATH: str = ""
FIG_WIDTH: int = 24 # Total width of entire figure image, in inches
FIG_HEIGHT: int = 18 # Total height of entire figure image, in inches
DEFAULT_FONT_FAMILY: str = "serif" # Default font family for all text in the figure
DEFAULT_SERIF_FONT: str = "cmr10" # Specific serif font to use for all text in the figure (cmr10 == Computer Modern Roman, the default LaTeX font)
DEFAULT_MATHTEXT_FONTSET: str = "cm" # Font set to use for "mathtext" aka latex-rendered labels (cm == Computer Modern)
DEFAULT_FONT_SIZE: float = 32 # Default font size for all text in the figure, in points
SUBPLOT_PADDING_X: float = 0.2 # Extra horizontal whitespace between subplots, in inches
SUBPLOT_PADDING_Y: float = 0.5 # Extra vertical whitespace between subplots, in inches
SUBPLOT_LETTER_OFFSET_X: float = -1.25 # Horizontal offset for subplot letter labels
SUBPLOT_LETTER_OFFSET_Y: float = 0.5 # Vertical offset for subplot letter labels
MARGIN_LEFT: float = 0.07 # Left margin as a fraction of figure width
MARGIN_RIGHT: float = 0.03 # Right margin as a fraction of figure width
MARGIN_TOP: float = 0.06 # Top margin as a fraction of figure height
MARGIN_BOTTOM: float = 0.08 # Bottom margin as a fraction of figure height
X_TICKS: list[float] = [0.3, 0.5, 0.7, 0.9, 1.1]
Y_TICKS: list[float] = [0.5, 1.0, 1.5]
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
    data: dict[float, float]

def build_subplot(all_profiles: list[Profile], temperature: int, time: TimePeriod, ax: Axes) -> None:
    profile_group: list[Profile] = [profile for profile in all_profiles if profile.temperature == temperature and profile.time_period == time]
    for concentration in [8, 16, 24]:
        for substance in [Substance.NACL, Substance.H2O]:
            profile = next(profile for profile in profile_group if profile.concentration == concentration and profile.substance == substance)
            line_color: str = "black" if concentration == 8 else "red" if concentration == 16 else "blue"
            line_style: str = "-" if substance == Substance.NACL else "--"
            ax.plot(list(profile.data.keys()), list(profile.data.values()), label=f"{concentration}% {substance.value}", color=line_color, linestyle=line_style)
    ax.set_xlabel(r"$r^*$")
    ax.set_xticks(X_TICKS)
    ax.set_xlim(X_TICKS[0], X_TICKS[-1])
    ax.set_ylabel(r"$\rho^*$")
    ax.set_ylim(0, YLIM_MAX)
    ax.set_yticks(Y_TICKS)

profiles: list[Profile] = []
for time in [TimePeriod.EARLY, TimePeriod.MID, TimePeriod.LATE]:
    for temperature in [25, 80]:
        for concentration in [8, 16, 24]:
            for substance in [Substance.NACL, Substance.H2O]:
                profiles.append(Profile(concentration, temperature, time, substance, {}))

with open(CSV_PATH, "r") as csv_file:
    reader = csv.reader(csv_file)
    next(reader)  # Skip header row
    for row in reader:
        profile_index: int = 0
        for i in range (1, len(row), 3):
            r_star = float(row[i])
            profiles[profile_index].data[r_star] = float(row[i + 1])
            profile_index += 1
            profiles[profile_index].data[r_star] = float(row[i + 2])
            profile_index += 1

plt.rc("font", family=DEFAULT_FONT_FAMILY, serif=DEFAULT_SERIF_FONT, size=DEFAULT_FONT_SIZE)
plt.rc("mathtext", fontset=DEFAULT_MATHTEXT_FONTSET)
fig, axes = plt.subplots(3, 2, figsize=(FIG_WIDTH, FIG_HEIGHT), gridspec_kw={'hspace': SUBPLOT_PADDING_Y, 'wspace': SUBPLOT_PADDING_X})
fig.subplots_adjust(left=MARGIN_LEFT, right=1.0 - MARGIN_RIGHT, top=1.0 - MARGIN_TOP, bottom=MARGIN_BOTTOM)
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