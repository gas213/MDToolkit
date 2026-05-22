"""
Generate a discretized color gradient map for use in OVITO or other visualization tools.
"""

import colorsys
from PIL import Image, ImageDraw

# --- Configuration ---
START_COLOR = "#00ff00"
END_COLOR   = "#005a00"
LEVELS      = 16
COLORSPACE  = "rgb"    # "rgb" or "hsv"
OUTPUT_PNG  = ""
BAND_WIDTH  = 64       # pixels wide per discrete color band
BAND_HEIGHT = 64       # image height in pixels
# ---------------------

def hex_to_rgb(hex_color: str) -> tuple[float, float, float]:
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    return r, g, b

def rgb_to_hex(r: float, g: float, b: float) -> str:
    return "#{:02x}{:02x}{:02x}".format(int(r * 255), int(g * 255), int(b * 255))

def generate_discrete_gradient(
    start_color: str,
    end_color: str,
    levels: int,
    colorspace: str = "rgb",
) -> list[dict]:
    """Return a list of discrete color stops evenly spaced between start and end."""
    r0, g0, b0 = hex_to_rgb(start_color)
    r1, g1, b1 = hex_to_rgb(end_color)

    colors = []
    for i in range(levels):
        t = i / (levels - 1) if levels > 1 else 0.0

        if colorspace == "hsv":
            h0, s0, v0 = colorsys.rgb_to_hsv(r0, g0, b0)
            h1, s1, v1 = colorsys.rgb_to_hsv(r1, g1, b1)
            h = h0 + t * (h1 - h0)
            s = s0 + t * (s1 - s0)
            v = v0 + t * (v1 - v0)
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
        else:  # linear RGB
            r = r0 + t * (r1 - r0)
            g = g0 + t * (g1 - g0)
            b = b0 + t * (b1 - b0)

        colors.append({
            "index": i,
            "position": round(t, 6),
            "hex": rgb_to_hex(r, g, b),
            "rgb": (round(r, 4), round(g, 4), round(b, 4)),
            "rgb255": (round(r * 255), round(g * 255), round(b * 255)),
        })

    return colors

def save_gradient_png(colors: list[dict], path: str, band_width: int = 64, height: int = 64) -> None:
    """Save the discretized gradient as a PNG with one band per color level."""
    img = Image.new("RGB", (len(colors) * band_width, height))
    draw = ImageDraw.Draw(img)
    for c in colors:
        r8, g8, b8 = c["rgb255"]
        x0 = c["index"] * band_width
        draw.rectangle([x0, 0, x0 + band_width - 1, height - 1], fill=(r8, g8, b8))
    img.save(path)
    print(f"Saved gradient to {path}")


colors = generate_discrete_gradient(START_COLOR, END_COLOR, LEVELS, COLORSPACE)
save_gradient_png(colors, OUTPUT_PNG, BAND_WIDTH, BAND_HEIGHT)
