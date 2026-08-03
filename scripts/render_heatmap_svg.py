#!/usr/bin/env python3
"""Render assets/contrib-heatmap.svg from data/contributions.json.

Draws the classic GitHub contribution graph: 7 weekday rows (Sunday on
top) x week columns, with a diagonal reveal animation (CSS keyframes).
Preview with STATIC=1 to emit a frozen frame.

Run with:  python scripts/render_heatmap_svg.py
"""

import json
import os
import xml.dom.minidom
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "contributions.json")
OUT = os.path.join(ROOT, "assets", "contrib-heatmap.svg")

VIEW_W = 860
CELL = 13
GAP = 3
PITCH = CELL + GAP
RX = 3

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
DOT_RED = "#EF4444"
DOT_AMBER = "#F59E0B"
DOT_GREEN = "#22C55E"
TITLE = "#93C5FD"
TEXT = "#E2E8F0"
BG = "#0B1020"
DIVIDER = "#1E3A8A"
LEGEND_TEXT = "#8B9DC3"

TITLE_BAR_H = 44
CAL_Y = 64


def load_days() -> tuple[dict[str, int], dict]:
    with open(DATA, encoding="utf-8") as fh:
        payload = json.load(fh)
    days = {d["date"]: d["level"] for d in payload["days"]}
    return days, payload["stats"]


def grid_columns(days: dict[str, int]) -> int:
    min_date = date.fromisoformat(min(days))
    max_date = date.fromisoformat(max(days))
    start = min_date - timedelta(days=(min_date.weekday() + 1) % 7)
    return ((max_date - start).days // 7) + 1


def month_of(d: str) -> str:
    return d[:7]


def build_svg(days: dict[str, int], stats: dict, static: bool) -> str:
    min_date = date.fromisoformat(min(days))
    start = min_date - timedelta(days=(min_date.weekday() + 1) % 7)

    cols = grid_columns(days)
    graph_w = cols * PITCH - GAP
    x0 = (VIEW_W - graph_w) / 2

    legend_y = CAL_Y + 7 * PITCH - GAP + 18
    footer_y = legend_y + 26
    height = footer_y + 16

    parts = []
    parts.append(
        f'<svg viewBox="0 0 {VIEW_W} {height}" '
        f'width="{VIEW_W}" height="{height}" '
        'xmlns="http://www.w3.org/2000/svg" xml:space="preserve" '
        'font-family="JetBrains Mono, Consolas, monospace">'
    )

    if not static:
        parts.append("  <defs>")
        parts.append("    <style>")
        parts.append("      .cell {")
        parts.append("        transform-box: fill-box;")
        parts.append(f"        animation: pop {0.45}s cubic-bezier(0.22,1,0.36,1) forwards;")
        parts.append("      }")
        parts.append("      @keyframes pop {")
        parts.append("        from { opacity: 0; transform: translate(-8px, -5px); }")
        parts.append("        to   { opacity: 1; transform: translate(0, 0); }")
        parts.append("      }")
        parts.append("    </style>")
        parts.append("  </defs>")

    parts.append(f'  <rect width="{VIEW_W}" height="{height}" rx="14" fill="{BG}" />')

    # Window title bar
    for cx, color in ((30, DOT_RED), (50, DOT_AMBER), (70, DOT_GREEN)):
        parts.append(f'  <circle cx="{cx}" cy="22" r="5" fill="{color}" />')
    parts.append(
        f'  <text x="{VIEW_W / 2:.0f}" y="27" text-anchor="middle" font-size="13" '
        f'font-weight="600" fill="{TITLE}" letter-spacing="1">contributions.sh</text>'
    )
    parts.append(
        f'  <line x1="14" y1="{TITLE_BAR_H}" x2="{VIEW_W - 14}" y2="{TITLE_BAR_H}" '
        f'stroke="{DIVIDER}" stroke-width="1" />'
    )

    for date_str, level in sorted(days.items()):
        d = date.fromisoformat(date_str)
        col = (d - start).days // 7
        row = (d.weekday() + 1) % 7
        x = x0 + col * PITCH
        y = CAL_Y + row * PITCH
        delay = f"{(col + row) * 0.014:.3f}s"
        parts.append(
            f'  <rect class="cell" x="{x:.1f}" y="{y:.1f}" width="{CELL}" '
            f'height="{CELL}" rx="{RX}" fill="{PALETTE[level]}" '
            f'style="animation-delay:{delay}" />'
        )

    # Legend: Less -> More
    legend_x = x0 + graph_w
    label_size = 11
    gap_label = 10
    boxes_right = legend_x - 30 - gap_label
    box1_x = boxes_right - CELL - 3 * PITCH
    box_y = legend_y - 8
    parts.append(
        f'  <text x="{box1_x - gap_label:.1f}" y="{legend_y:.1f}" text-anchor="end" '
        f'font-size="{label_size}" fill="{LEGEND_TEXT}">Less</text>'
    )
    for lvl in (1, 2, 3, 4):
        bx = boxes_right - CELL - (4 - lvl) * PITCH
        parts.append(
            f'  <rect x="{bx:.1f}" y="{box_y:.1f}" width="{CELL}" height="{CELL}" '
            f'rx="{RX}" fill="{PALETTE[lvl]}" />'
        )
    parts.append(
        f'  <text x="{boxes_right + gap_label:.1f}" y="{legend_y:.1f}" '
        f'font-size="{label_size}" fill="{LEGEND_TEXT}">More</text>'
    )

    total = stats.get("total", 0)
    label = f"{total:,} contributions in the last year".replace(",", " ")
    parts.append(
        f'  <text x="{VIEW_W / 2:.0f}" y="{footer_y:.1f}" text-anchor="middle" '
        f'font-size="13" fill="{TEXT}">{label}</text>'
    )

    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    days, stats = load_days()
    static = os.environ.get("STATIC") == "1"
    svg = build_svg(days, stats, static=static)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(svg + "\n")
    xml.dom.minidom.parse(OUT)
    print(f"wrote {OUT} ({len(days)} days, {grid_columns(days)} columns)"
          + (" (static frame)" if static else ""))


if __name__ == "__main__":
    main()
