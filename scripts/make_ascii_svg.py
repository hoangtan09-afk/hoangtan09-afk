from pathlib import Path
from PIL import Image, ImageOps
from html import escape

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT = BASE_DIR / "assets" / "avatar-prepped.png"
OUTPUT = BASE_DIR / "assets" / "avatar-ascii.svg"

# Nhieu muc sang/toi hon -> chi tiet tot hon
RAMP = " .`:-=+*cs#%@"

ASCII_WIDTH = 115

FONT_SIZE = 10
CHAR_WIDTH = 6.0
LINE_HEIGHT = 10

# Terminal panel
PANEL_WIDTH = 420
PANEL_HEIGHT = 460

# Khoang trong quanh nguoi sau khi crop
CROP_PADDING = 20


image = Image.open(INPUT).convert("RGBA")

# =========================================================
# 1. CROP SAT VUNG NGUOI
# =========================================================

alpha = image.getchannel("A")
bbox = alpha.getbbox()

if bbox is None:
    raise ValueError("Khong tim thay foreground trong anh.")

left, top, right, bottom = bbox

left = max(0, left - CROP_PADDING)
top = max(0, top - CROP_PADDING)
right = min(image.width, right + CROP_PADDING)
bottom = min(image.height, bottom + CROP_PADDING)

image = image.crop((left, top, right, bottom))


# =========================================================
# 2. GRAYSCALE + CONTRAST
# =========================================================

alpha = image.getchannel("A")

gray = image.convert("L")
gray = ImageOps.autocontrast(gray)

image = Image.merge(
    "RGBA",
    (gray, gray, gray, alpha)
)


# =========================================================
# 3. RESIZE CHO ASCII
# =========================================================

original_width, original_height = image.size

aspect_ratio = original_height / original_width

ascii_height = int(
    ASCII_WIDTH * aspect_ratio * 0.52
)

image = image.resize(
    (ASCII_WIDTH, ascii_height),
    Image.Resampling.LANCZOS
)

pixels = image.load()

ascii_lines = []


# =========================================================
# 4. CONVERT PIXEL -> ASCII
# =========================================================

for y in range(ascii_height):

    line = ""

    for x in range(ASCII_WIDTH):

        r, g, b, a = pixels[x, y]

        # Pixel trong suot
        if a < 40:
            line += " "
            continue

        brightness = (r + g + b) / 3

        # Xac dinh vung mat: phan tren cua nhan vat
        face_zone = y < ascii_height * 0.60

        if face_zone:
            # Vung mat: de trong nhieu hon de co negative space
            if brightness > 175:
                line += " "
                continue
            elif brightness > 155:
                line += " "
                continue
            elif brightness > 138:
                line += "."
                continue
            elif brightness > 122:
                line += ":"
                continue

            darkness = (122 - brightness) / 122
            darkness = max(0, min(darkness, 1))

            SHADOW_RAMP = "-=+*#%@"
            index = int(darkness * (len(SHADOW_RAMP) - 1))
            line += SHADOW_RAMP[index]

        else:
            # Vung ao/co/vai: giu chi tiet hon
            if brightness > 190:
                line += " "
                continue
            elif brightness > 165:
                line += "."
                continue
            elif brightness > 140:
                line += ":"
                continue

            darkness = (140 - brightness) / 140
            darkness = max(0, min(darkness, 1))

            SHADOW_RAMP = "-=+*cs#%@"
            index = int(darkness * (len(SHADOW_RAMP) - 1))
            line += SHADOW_RAMP[index]

    ascii_lines.append(line)


# =========================================================
# 5. TINH SCALE VA CAN GIUA
# =========================================================

ascii_original_width = ASCII_WIDTH * CHAR_WIDTH
ascii_original_height = ascii_height * LINE_HEIGHT

content_width = PANEL_WIDTH - 30
content_height = PANEL_HEIGHT - 70

scale_x = content_width / ascii_original_width
scale_y = content_height / ascii_original_height

scale = min(scale_x, scale_y)

scaled_width = ascii_original_width * scale
scaled_height = ascii_original_height * scale

# Can chinh giua terminal
offset_x = (PANEL_WIDTH - scaled_width) / 2
offset_y = 55 + ((PANEL_HEIGHT - 55 - scaled_height) / 2)


# =========================================================
# 6. SVG
# =========================================================

svg = f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="{PANEL_WIDTH}"
height="{PANEL_HEIGHT}"
viewBox="0 0 {PANEL_WIDTH} {PANEL_HEIGHT}">

<rect
    x="1"
    y="1"
    width="{PANEL_WIDTH - 2}"
    height="{PANEL_HEIGHT - 2}"
    rx="14"
    fill="#0d1117"
    stroke="#30363d"
/>

<!-- Terminal top bar -->
<line
    x1="1"
    y1="42"
    x2="{PANEL_WIDTH - 1}"
    y2="42"
    stroke="#30363d"
/>

<!-- Terminal buttons -->
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
    delay = i * 0.020

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