#!/usr/bin/env python3
"""Generate assets/info-card.svg — a neofetch-style profile panel.

Renders the profile data as a terminal window with a title bar and
key/value rows. Lines fade+slide in with a short stagger (CSS keyframes,
no loop). Preview with STATIC=1 to emit a frozen, fully-visible frame:

  STATIC=1 python scripts/make_info_card.py
"""

import os
import xml.dom.minidom

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets", "info-card.svg")

WIDTH = 490
BG = "#0B1020"
KEY = "#93C5FD"
VALUE = "#E2E8F0"
TITLE = "#E2E8F0"
DIVIDER = "#1E3A8A"
DOT_RED = "#EF4444"
DOT_AMBER = "#F59E0B"
DOT_GREEN = "#22C55E"

FONT = 14.0
CHAR_W = FONT * 0.6
LINE_H = 22.0
KEY_X = 24.0
VALUE_X = 138.0
PAD_R = 22.0
STAGGER = 0.15
EASING = "cubic-bezier(0.22,1,0.36,1)"

ROWS = [
    ("User:", "luisdiaz04"),
    ("Name:", "Luis \u00c1ngel D\u00edaz D\u00edaz"),
    ("Role:", "Software Engineer \u00b7 Full-Stack"),
    ("Location:", "Oaxaca, Mexico"),
    (
        "Stack:",
        "TypeScript \u00b7 JavaScript \u00b7 React \u00b7 Node.js \u00b7 "
        "PostgreSQL \u00b7 MongoDB \u00b7 Docker \u00b7 Kubernetes \u00b7 "
        "GitHub Actions",
    ),
    (
        "Focus:",
        "REST APIs \u00b7 System Design \u00b7 Clean Architecture \u00b7 Cloud-Native",
    ),
]

TITLE_BAR = 44.0
BODY_TOP = 70.0


def wrap(text: str, max_chars: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for word in words:
        candidate = f"{cur} {word}".strip()
        if len(candidate) <= max_chars:
            cur = candidate
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines or [""]


def max_chars_for() -> int:
    usable = WIDTH - VALUE_X - PAD_R
    return max(1, int(usable // CHAR_W))


def render_lines() -> list[tuple[str, list[str]]]:
    maxc = max_chars_for()
    return [(key, wrap(value, maxc)) for key, value in ROWS]


def build_svg(lines: list[tuple[str, list[str]]], static: bool) -> str:
    total_lines = sum(len(v) for _, v in lines)
    height = BODY_TOP + total_lines * LINE_H + 20

    parts = []
    parts.append(
        f'<svg viewBox="0 0 {WIDTH} {height:.0f}" '
        f'width="{WIDTH}" height="{height:.0f}" '
        'xmlns="http://www.w3.org/2000/svg" xml:space="preserve" '
        'font-family="JetBrains Mono, Consolas, monospace">'
    )

    if not static:
        parts.append("  <defs>")
        parts.append("    <style>")
        parts.append("      .ln {")
        parts.append("        transform-box: fill-box;")
        parts.append(f"        animation: fadeUp {0.5}s {EASING} forwards;")
        parts.append("      }")
        parts.append("      @keyframes fadeUp {")
        parts.append("        from { opacity: 0; transform: translateY(8px); }")
        parts.append("        to   { opacity: 1; transform: translateY(0); }")
        parts.append("      }")
        parts.append("    </style>")
        parts.append("  </defs>")

    parts.append(f'  <rect width="{WIDTH}" height="{height:.0f}" rx="14" fill="{BG}" />')

    # Title bar
    for cx, color in ((30, DOT_RED), (50, DOT_AMBER), (70, DOT_GREEN)):
        parts.append(f'  <circle cx="{cx}" cy="22" r="5" fill="{color}" />')
    parts.append(
        f'  <text x="{WIDTH / 2:.0f}" y="27" text-anchor="middle" '
        f'font-size="13" font-weight="600" fill="{TITLE}" '
        'letter-spacing="1">luis@github: ~/profile</text>'
    )
    parts.append(
        f'  <line x1="14" y1="{TITLE_BAR}" x2="{WIDTH - 14}" y2="{TITLE_BAR}" '
        f'stroke="{DIVIDER}" stroke-width="1" />'
    )

    idx = 0
    y = BODY_TOP
    for key, value_lines in lines:
        parts.append(
            f'  <text class="ln" x="{KEY_X:.0f}" y="{y:.0f}" font-size="{FONT:.0f}" '
            f'font-weight="600" fill="{KEY}" style="animation-delay:{idx * STAGGER:.2f}s">'
            f"{key}</text>"
        )
        idx += 1
        for line in value_lines:
            parts.append(
                f'  <text class="ln" x="{VALUE_X:.0f}" y="{y:.0f}" font-size="{FONT:.0f}" '
                f'fill="{VALUE}" style="animation-delay:{idx * STAGGER:.2f}s">'
                f"{line}</text>"
            )
            idx += 1
            y += LINE_H
        y += 4

    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    static = os.environ.get("STATIC") == "1"
    svg = build_svg(render_lines(), static=static)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(svg + "\n")
    xml.dom.minidom.parse(OUT)
    print(f"wrote {OUT}" + (" (static frame)" if static else ""))


if __name__ == "__main__":
    main()
