from pathlib import Path
from PIL import Image, ImageOps
from html import escape

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT = BASE_DIR / "assets" / "avatar-prepped.png"
OUTPUT = BASE_DIR / "assets" / "avatar-ascii.svg"

RAMP = " .:-=+*#%@"
ASCII_WIDTH = 95

FONT_SIZE = 11
CHAR_WIDTH = 6.6
LINE_HEIGHT = 11

image = Image.open(INPUT).convert("RGBA")

alpha = image.getchannel("A")
gray = image.convert("L")
gray = ImageOps.autocontrast(gray)

image = Image.merge("RGBA", (gray, gray, gray, alpha))

original_width, original_height = image.size

aspect_ratio = original_height / original_width
ascii_height = int(ASCII_WIDTH * aspect_ratio * 0.55)

image = image.resize((ASCII_WIDTH, ascii_height))

pixels = image.load()

ascii_lines = []

for y in range(ascii_height):
    line = ""

    for x in range(ASCII_WIDTH):
        r, g, b, a = pixels[x, y]

        if a < 40:
            line += " "
            continue

        brightness = (r + g + b) / 3
        brightness = min(255, brightness * 1.15)

        index = int(
            (255 - brightness)
            / 255
            * (len(RAMP) - 1)
        )

        index = max(0, min(index, len(RAMP) - 1))

        line += RAMP[index]

    ascii_lines.append(line)

svg_width = int(ASCII_WIDTH * CHAR_WIDTH)
svg_height = int(ascii_height * LINE_HEIGHT)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{svg_width}"
height="{svg_height}"
viewBox="0 0 {svg_width} {svg_height}">

<rect width="100%" height="100%" fill="#0d1117"/>

<style>

text {{
    font-family: Consolas, "Courier New", monospace;
    font-size: {FONT_SIZE}px;
    fill: #c9d1d9;
    white-space: pre;
}}

.line {{
    opacity: 0;
    animation: appear 0.15s forwards;
}}

@keyframes appear {{
    from {{
        opacity: 0;
    }}

    to {{
        opacity: 1;
    }}
}}

</style>
'''

for i, line in enumerate(ascii_lines):

    y = (i + 1) * LINE_HEIGHT

    delay = i * 0.025

    svg += f'''
<text
    class="line"
    x="0"
    y="{y}"
    style="animation-delay:{delay:.3f}s"
>{escape(line)}</text>
'''

svg += "</svg>"

OUTPUT.write_text(svg, encoding="utf-8")

print(f"Done: {OUTPUT}")
print(f"ASCII size: {ASCII_WIDTH} x {ascii_height}")