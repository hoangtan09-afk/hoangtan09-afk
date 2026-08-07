from pathlib import Path
from html import escape

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT = BASE_DIR / "assets" / "info-card.svg"

WIDTH = 720
HEIGHT = 460

lines = [
    ("OS", "Windows 11 / Ubuntu"),
    ("Education", "FPT University"),
    ("Role", "Information Assurance"),
    ("Focus", "Blue Team / SOC"),
    ("Learning", "Network Analysis / Digital Forensics"),
    ("Stack", "Python / Linux / Wazuh"),
]

svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<rect
    width="100%"
    height="100%"
    rx="18"
    fill="#0d1117"
    stroke="#30363d"
/>

<!-- Terminal top bar -->
<line
    x1="0"
    y1="48"
    x2="{WIDTH}"
    y2="48"
    stroke="#30363d"
/>

<!-- Window buttons -->
<circle cx="22" cy="24" r="6" fill="#ff5f56"/>
<circle cx="42" cy="24" r="6" fill="#ffbd2e"/>
<circle cx="62" cy="24" r="6" fill="#27c93f"/>

<!-- Terminal title -->
<text
    x="360"
    y="29"
    text-anchor="middle"
    font-family="Consolas, Courier New, monospace"
    font-size="14"
    fill="#8b949e"
>
hoangtan09-afk@github: ~ $ ./whoami
</text>

<style>

.label {{
    font-family: Consolas, "Courier New", monospace;
    font-size: 19px;
    font-weight: bold;
    fill: #58a6ff;
}}

.value {{
    font-family: Consolas, "Courier New", monospace;
    font-size: 19px;
    fill: #c9d1d9;
}}

.prompt {{
    font-family: Consolas, "Courier New", monospace;
    font-size: 22px;
    font-weight: bold;
    fill: #7ee787;
}}

.line {{
    opacity: 0;
    animation: appear 0.4s forwards;
}}

@keyframes appear {{
    from {{
        opacity: 0;
        transform: translateX(-8px);
    }}

    to {{
        opacity: 1;
        transform: translateX(0);
    }}
}}

</style>

<!-- Prompt -->
<text
    class="prompt"
    x="55"
    y="105"
>
hoangtan09-afk@github ~ $ whoami
</text>
'''

start_y = 165
line_height = 45

for i, (label, value) in enumerate(lines):
    y = start_y + i * line_height
    delay = 0.35 + i * 0.18

    svg += f'''
<g class="line" style="animation-delay:{delay:.2f}s">

    <text
        class="label"
        x="55"
        y="{y}"
    >
        {escape(label)}
    </text>

    <text
        class="value"
        x="190"
        y="{y}"
    >
        {escape(value)}
    </text>

</g>
'''

svg += "\n</svg>"

OUTPUT.write_text(svg, encoding="utf-8")

print(f"Done: {OUTPUT}")