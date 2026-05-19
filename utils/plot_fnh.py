# Plot first-neighbor histograms for paper
import csv
from dataclasses import dataclass
from enum import Enum
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
from matplotlib.transforms import ScaledTranslation
import numpy as np
import os.path

CSV_PATH: str = ""
FIG_WIDTH: int = 24 # Total width of entire figure image, in inches
FIG_HEIGHT: int = 18 # Total height of entire figure image, in inches
DEFAULT_FONT_FAMILY: str = "serif" # Default font family for all text in the figure
DEFAULT_SERIF_FONT: str = "cmr10" # Specific serif font to use for all text in the figure (cmr10 == Computer Modern Roman, the default LaTeX font)
DEFAULT_FONT_SIZE: float = 24 # Default font size for all text in the figure, in points
SUBPLOT_PADDING_X: float = 0.2 # Extra horizontal whitespace between subplots, in inches
SUBPLOT_PADDING_Y: float = 0.5 # Extra vertical whitespace between subplots, in inches
SUBPLOT_LETTER_OFFSET_X: float = -1.0 # Horizontal offset for subplot letter labels
SUBPLOT_LETTER_OFFSET_Y: float = 0.5 # Vertical offset for subplot letter labels
BAR_WIDTH: float = 0.1 # Width of each bar in the histogram plots
BAR_GAP: float = 0.035 # Gap between each bar within a cluster
YLIM_MAX: float = 0.42 # Maximum y-axis limit for all subplots
YTICK_SIZE: float = 0.1 # Interval between y-axis ticks for all subplots

class TimePeriod(Enum):
    EARLY = "Early"
    MID = "Mid"
    LATE = "Late"

class Region(Enum):
    BULK = "Bulk"
    SHELL = "Shell"

@dataclass
class Histogram:
    concentration: int
    temperature: int
    time_period: TimePeriod
    region: Region
    data: dict[int, float]

def build_subplot(all_histograms: list[Histogram], concentration: int, temperature: int, ax: Axes) -> None:
    hist_group: list[Histogram] = [hist for hist in all_histograms if hist.concentration == concentration and hist.temperature == temperature]
    offset: float = -2.5 * (BAR_WIDTH + BAR_GAP)
    for time in [TimePeriod.EARLY, TimePeriod.MID, TimePeriod.LATE]:
        for region in [Region.BULK, Region.SHELL]:
            hist = next(hist for hist in hist_group if hist.time_period == time and hist.region == region)
            pair_color: str = "black" if time == TimePeriod.EARLY else "red" if time == TimePeriod.MID else "blue"
            fill_color: str = pair_color if region == Region.BULK else "white"
            edge_color: str = "none" if hist.region == Region.BULK else pair_color
            ax.bar([float(i) + offset for i in hist.data.keys()], list(hist.data.values()), width=BAR_WIDTH, color=fill_color, edgecolor=edge_color)
            offset += BAR_WIDTH + BAR_GAP
    ax.set_title(f"{concentration}% at {temperature} C")
    ax.set_xlabel("Number of Cl First Neighbors")
    ax.set_xticks(list(hist_group[0].data.keys()))
    ax.set_ylabel("Probability")
    ax.set_ylim(0, YLIM_MAX)
    ax.set_yticks(np.arange(0, YLIM_MAX, YTICK_SIZE))

histograms: list[Histogram] = []
with open(CSV_PATH, "r") as csv_file:
    reader = csv.reader(csv_file)
    next(reader)  # Skip header row
    for row in reader:
        concentration = int(row[0])
        temperature = int(row[1])
        time_period = TimePeriod(row[2])
        region = Region(row[3])
        data = {i: float(row[i + 4]) for i in range(7)}
        histograms.append(Histogram(concentration, temperature, time_period, region, data))

plt.rc("font", family=DEFAULT_FONT_FAMILY, serif=DEFAULT_SERIF_FONT, size=DEFAULT_FONT_SIZE)
fig, axes = plt.subplots(3, 2, figsize=(FIG_WIDTH, FIG_HEIGHT), gridspec_kw={'hspace': SUBPLOT_PADDING_Y, 'wspace': SUBPLOT_PADDING_X})
build_subplot(histograms, 8, 25, axes[0, 0])
build_subplot(histograms, 8, 80, axes[0, 1])
build_subplot(histograms, 16, 25, axes[1, 0])
build_subplot(histograms, 16, 80, axes[1, 1])
build_subplot(histograms, 24, 25, axes[2, 0])
build_subplot(histograms, 24, 80, axes[2, 1])

letters = ["a)", "b)", "c)", "d)", "e)", "f)"]
for i, ax in enumerate(axes.flat):
    offset = ScaledTranslation(SUBPLOT_LETTER_OFFSET_X, SUBPLOT_LETTER_OFFSET_Y, fig.dpi_scale_trans)
    ax.text(0.0, 1.0, letters[i], transform=ax.transAxes + offset)

plt.savefig(os.path.splitext(CSV_PATH)[0] + ".png")