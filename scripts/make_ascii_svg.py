#!/usr/bin/env python3
"""Generate assets/astronaut-ascii.svg from assets/astronaut.png.

Renders the astronaut as a monochrome ASCII portrait where each row is
revealed left-to-right with a staggered typing effect. All animation lives
inside the SVG (CSS keyframes), so GitHub renders it without JavaScript.

Re-run with:  python scripts/make_ascii_svg.py
"""

import os
import xml.dom.minidom

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "assets", "astronaut.png")
OUT = os.path.join(ROOT, "assets", "astronaut-ascii.svg")

RAMP = " .`:-=+*cs#%@"

COLOR = "#60A5FA"
CURSOR = "#93C5FD"
BG = "#0B1020"

COLS = int(os.environ.get("ASCII_COLS", "68"))
MARGIN = 16
FONT_SIZE = 9.0
CHAR_W = FONT_SIZE * 0.6
LINE_H = FONT_SIZE * 1.2
STAGGER = 0.07
DURATION = 0.5
EASING = "cubic-bezier(0.22,1,0.36,1)"


def image_to_rows(path: str, cols: int) -> list[str]:
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    bg = Image.new("RGB", img.size, (255, 255, 255))
    bg.paste(img, mask=img.split()[3])
    gray = bg.convert("L")

    rows = max(1, round(cols * (h / w) * (CHAR_W / LINE_H)))
    gray = gray.resize((cols, rows), Image.LANCZOS)

    ramp = list(RAMP)
    denom = max(1, len(ramp) - 1)
    out = []
    for y in range(rows):
        line = []
        for x in range(cols):
            value = gray.getpixel((x, y))
            idx = (255 - value) * denom // 255
            line.append(ramp[idx])
        out.append("".join(line))
    return out


def build_svg(rows: list[str]) -> str:
    rows_n = len(rows)
    text_w = COLS * CHAR_W
    view_w = text_w + 2 * MARGIN
    view_h = rows_n * LINE_H + 2 * MARGIN

    parts = []
    parts.append(
        f'<svg viewBox="0 0 {view_w:.1f} {view_h:.1f}" '
        f'width="{view_w:.0f}" height="{view_h:.0f}" '
        'xmlns="http://www.w3.org/2000/svg" xml:space="preserve" '
        'font-family="JetBrains Mono, Consolas, monospace">'
    )
    parts.append("  <defs>")
    parts.append("    <style>")
    parts.append("      .ascii-row {")
    parts.append(f"        fill: {COLOR};")
    parts.append(f"        font-size: {FONT_SIZE}px;")
    parts.append("        white-space: pre;")
    parts.append("        text-anchor: start;")
    parts.append("      }")
    parts.append("      .wipe {")
    parts.append("        transform-box: fill-box;")
    parts.append("        transform-origin: left center;")
    parts.append(f"        animation: wipe {DURATION}s {EASING} forwards;")
    parts.append("      }")
    parts.append("      .cur {")
    parts.append(f"        fill: {CURSOR};")
    parts.append("        opacity: 0;")
    parts.append("        transform-box: fill-box;")
    parts.append("        transform-origin: left center;")
    parts.append(f"        animation: slide {DURATION}s {EASING} forwards;")
    parts.append("      }")
    parts.append("      @keyframes wipe {")
    parts.append("        from { transform: scaleX(0); }")
    parts.append("        to   { transform: scaleX(1); }")
    parts.append("      }")
    parts.append("      @keyframes slide {")
    parts.append("        from { transform: translateX(0); opacity: 0; }")
    parts.append("        10%  { opacity: 1; }")
    parts.append(f"        to   {{ transform: translateX({text_w - CHAR_W:.1f}px); opacity: 1; }}")
    parts.append("      }")
    parts.append("    </style>")
    for i, row in enumerate(rows):
        parts.append(f'    <clipPath id="cp{i}">')
        parts.append(
            f'      <rect class="wipe" x="{MARGIN:.1f}" y="{MARGIN + i * LINE_H:.1f}" '
            f'width="{text_w:.1f}" height="{LINE_H:.1f}" '
            f'style="animation-delay:{i * STAGGER:.2f}s" />'
        )
        parts.append("    </clipPath>")
    parts.append("  </defs>")

    parts.append(f'  <rect width="{view_w:.1f}" height="{view_h:.1f}" rx="14" fill="{BG}" />')

    for i, row in enumerate(rows):
        top = MARGIN + i * LINE_H
        baseline = top + FONT_SIZE * 0.8
        delay = f"{i * STAGGER:.2f}s"
        parts.append(
            f'  <text class="ascii-row" x="{MARGIN:.1f}" y="{baseline:.1f}" '
            f'clip-path="url(#cp{i})">{row}</text>'
        )
        parts.append(
            f'  <rect class="cur" x="{MARGIN:.1f}" y="{top + 1:.1f}" '
            f'width="{CHAR_W:.1f}" height="{LINE_H - 2:.1f}" rx="1" '
            f'style="animation-delay:{delay}" />'
        )

    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    rows = image_to_rows(SRC, COLS)
    svg = build_svg(rows)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(svg + "\n")

    # Trim trailing whitespace-only rows so the box hugs the artwork.
    xml.dom.minidom.parse(OUT)
    print(f"wrote {OUT} ({COLS}x{len(rows)} chars)")


if __name__ == "__main__":
    main()
