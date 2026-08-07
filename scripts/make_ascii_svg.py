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

# Kich thuoc terminal panel
PANEL_WIDTH = 420
PANEL_HEIGHT = 460

image = Image.open(INPUT).convert("RGBA")

alpha = image.getchannel("A")

gray = image.convert("L")
gray = ImageOps.autocontrast(gray)

image = Image.merge(
    "RGBA",
    (gray, gray, gray, alpha)
)

original_width, original_height = image.size

aspect_ratio = original_height / original_width

ascii_height = int(
    ASCII_WIDTH * aspect_ratio * 0.55
)

image = image.resize(
    (ASCII_WIDTH, ascii_height)
)

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

        # Tang sang nhe
        brightness = min(
            255,
            brightness * 1.15
        )

        index = int(
            (255 - brightness)
            / 255
            * (len(RAMP) - 1)
        )

        index = max(
            0,
            min(index, len(RAMP) - 1)
        )

        line += RAMP[index]

    ascii_lines.append(line)


# Kich thuoc goc cua khoi ASCII
ascii_original_width = ASCII_WIDTH * CHAR_WIDTH
ascii_original_height = ascii_height * LINE_HEIGHT

# Khu vuc ben trong terminal
content_width = PANEL_WIDTH - 35
content_height = PANEL_HEIGHT - 75

scale_x = content_width / ascii_original_width
scale_y = content_height / ascii_original_height

# Chon scale nho hon de anh khong bi meo
PORTRAIT_ZOOM = 1.18

scale = min(scale_x, scale_y) * PORTRAIT_ZOOM

scaled_width = ascii_original_width * scale
scaled_height = ascii_original_height * scale

# Can giua
offset_x = (PANEL_WIDTH - scaled_width) / 2
offset_y = 62 + ((PANEL_HEIGHT - 62 - scaled_height) / 2)


svg = f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="{PANEL_WIDTH}"
height="{PANEL_HEIGHT}"
viewBox="0 0 {PANEL_WIDTH} {PANEL_HEIGHT}">

<!-- Terminal background -->
<rect
    x="1"
    y="1"
    width="{PANEL_WIDTH - 2}"
    height="{PANEL_HEIGHT - 2}"
    rx="14"
    fill="#0d1117"
    stroke="#30363d"
/>

<!-- Top bar -->
<line
    x1="1"
    y1="42"
    x2="{PANEL_WIDTH - 1}"
    y2="42"
    stroke="#30363d"
/>

<!-- macOS-style buttons -->
<circle cx="18" cy="21" r="5" fill="#ff5f56"/>
<circle cx="34" cy="21" r="5" fill="#ffbd2e"/>
<circle cx="50" cy="21" r="5" fill="#27c93f"/>

<!-- Terminal title -->
<text
    x="{PANEL_WIDTH / 2}"
    y="26"
    text-anchor="middle"
    font-family="Consolas, Courier New, monospace"
    font-size="10"
    fill="#8b949e"
>
hoangtan09-afk@github: ~ $ ./portrait.sh
</text>

<style>

.ascii {{
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

<g transform="translate({offset_x:.2f} {offset_y:.2f}) scale({scale:.4f})">
'''

for i, line in enumerate(ascii_lines):

    y = (i + 1) * LINE_HEIGHT
    delay = i * 0.025

    svg += f'''
<text
    class="ascii line"
    x="0"
    y="{y}"
    style="animation-delay:{delay:.3f}s"
>{escape(line)}</text>
'''

svg += '''
</g>

</svg>
'''

OUTPUT.write_text(
    svg,
    encoding="utf-8"
)

print(f"Done: {OUTPUT}")
print(f"ASCII size: {ASCII_WIDTH} x {ascii_height}")
print(f"Scale: {scale:.3f}")