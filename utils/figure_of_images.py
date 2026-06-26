# Assemble a grid of images into a single figure for paper
import string
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.transforms import ScaledTranslation

# Paths to image files, in row-major order (left-to-right, top-to-bottom)
IMAGES: list[str] = [
    "path/to/example.png"
]

OUTPUT_PATH: str = "figure.png" # Output path for the saved figure
NUM_ROWS: int = 3 # Number of rows in the image grid
NUM_COLS: int = 3 # Number of columns in the image grid
FIG_WIDTH: int = 20 # Total width of entire figure image, in inches
FIG_HEIGHT: int = 18 # Total height of entire figure image, in inches
DEFAULT_FONT_FAMILY: str = "serif" # Default font family for all text in the figure
DEFAULT_SERIF_FONT: str = "cmr10" # Specific serif font to use for all text in the figure (cmr10 == Computer Modern Roman, the default LaTeX font)
DEFAULT_FONT_SIZE: float = 24 # Default font size for all text in the figure, in points
SUBPLOT_PADDING_X: float = 0.0 # Extra horizontal whitespace between subplots, in inches
SUBPLOT_PADDING_Y: float = 0.0 # Extra vertical whitespace between subplots, in inches
SUBPLOT_LETTER_OFFSET_X: float = -0.2 # Horizontal offset for subplot letter labels
SUBPLOT_LETTER_OFFSET_Y: float = -0.8 # Vertical offset for subplot letter labels
MARGIN_X: float = 0.02 # Left and right margin as a fraction of figure width
MARGIN_Y: float = 0.02 # Top and bottom margin as a fraction of figure height

plt.rc("font", family=DEFAULT_FONT_FAMILY, serif=DEFAULT_SERIF_FONT, size=DEFAULT_FONT_SIZE)
fig, axes = plt.subplots(NUM_ROWS, NUM_COLS, figsize=(FIG_WIDTH, FIG_HEIGHT), gridspec_kw={'hspace': SUBPLOT_PADDING_Y, 'wspace': SUBPLOT_PADDING_X})
fig.subplots_adjust(left=MARGIN_X, right=1.0 - MARGIN_X, top=1.0 - MARGIN_Y, bottom=MARGIN_Y)

for i, ax in enumerate(axes.flat):
    if i < len(IMAGES):
        ax.imshow(mpimg.imread(IMAGES[i]))
    ax.axis("off")

letters = [f"{c})" for c in string.ascii_lowercase]
for i, ax in enumerate(axes.flat):
    offset = ScaledTranslation(SUBPLOT_LETTER_OFFSET_X, SUBPLOT_LETTER_OFFSET_Y, fig.dpi_scale_trans)
    ax.text(0.0, 1.0, letters[i], transform=ax.transAxes + offset)

plt.savefig(OUTPUT_PATH)
