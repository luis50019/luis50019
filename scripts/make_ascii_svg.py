#!/usr/bin/env python3
"""Generate assets/astronaut-ascii.svg from assets/astronaut.png.

Renders the astronaut as a monochrome ASCII portrait where each row is
revealed left-to-right with a staggered typing effect.

The animation uses SMIL (<animate>) only, NOT CSS keyframes or clipPath
transforms: every row is a static <text> covered by a background-colored
"curtain" <rect> whose x coordinate animates, exposing the row underneath.
A small cursor block rides the reveal edge. SMIL is what GitHub reliably
executes inside SVGs rendered via <img>.

Re-run with:  python scripts/make_ascii_svg.py
Preview static frame with:  STATIC=1 python scripts/make_ascii_svg.py
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


def build_svg(rows: list[str], static: bool = False) -> str:
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
    parts.append("    </style>")
    parts.append("  </defs>")

    parts.append(f'  <rect width="{view_w:.1f}" height="{view_h:.1f}" rx="14" fill="{BG}" />')

    for i, row in enumerate(rows):
        top = MARGIN + i * LINE_H
        baseline = top + FONT_SIZE * 0.8
        begin = f"{i * STAGGER:.2f}s"

        # 1) Full row text (static, always present).
        parts.append(
            f'  <text class="ascii-row" x="{MARGIN:.1f}" y="{baseline:.1f}">{row}</text>'
        )
        if static:
            continue

        # 2) Curtain: background-colored rect covering the row. Its x moves
        #    left -> right via SMIL, exposing the text underneath.
        curtain_x = f'{MARGIN + text_w:.1f}' if static else f'{MARGIN:.1f}'
        parts.append(
            f'  <rect x="{curtain_x}" y="{top:.1f}" width="{text_w:.1f}" '
            f'height="{LINE_H:.1f}" fill="{BG}">'
        )
        parts.append(
            f'    <animate attributeName="x" '
            f'from="{MARGIN:.1f}" to="{MARGIN + text_w:.1f}" '
            f'begin="{begin}" dur="{DURATION}s" fill="freeze" />'
        )
        parts.append("  </rect>")

        # 3) Cursor block riding the reveal edge.
        parts.append(
            f'  <rect x="{MARGIN - CHAR_W:.1f}" y="{top + 1:.1f}" '
            f'width="{CHAR_W:.1f}" height="{LINE_H - 2:.1f}" rx="1" fill="{CURSOR}">'
        )
        parts.append(
            f'    <animate attributeName="x" '
            f'from="{MARGIN - CHAR_W:.1f}" to="{MARGIN + text_w - CHAR_W:.1f}" '
            f'begin="{begin}" dur="{DURATION}s" fill="freeze" />'
        )
        parts.append(
            f'    <animate attributeName="opacity" from="0" to="1" '
            f'begin="{begin}" dur="0.05s" fill="freeze" />'
        )
        parts.append("  </rect>")

    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    rows = image_to_rows(SRC, COLS)
    static = os.environ.get("STATIC") == "1"
    svg = build_svg(rows, static=static)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(svg + "\n")

    xml.dom.minidom.parse(OUT)
    print(f"wrote {OUT} ({COLS}x{len(rows)} chars)"
          + (" (static frame)" if static else ""))


if __name__ == "__main__":
    main()
