#!/usr/bin/env python3
"""Fetch GitHub contribution data for a profile and write data/contributions.json.

Uses the public contributions HTML fragment (no token required). If the
network fails or the HTML cannot be parsed, a deterministic example dataset
is written instead and a warning is printed to stderr.

Run with:  python scripts/fetch_contributions.py [username]
"""

import json
import os
import random
import re
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta

import requests
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "data", "contributions.json")

DEFAULT_USER = "luis50019"
URL = "https://github.com/users/{user}/contributions"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

EXAMPLE_DAYS = 364
EXAMPLE_SEED = 20260101


def compute_stats(days: list[dict]) -> dict:
    by_date = {d["date"]: d["level"] for d in days}
    total_levels = sum(d["level"] for d in days)

    today = date.today().isoformat()
    current = 0
    probe = date.today()
    if by_date.get(probe.isoformat(), 0) == 0:
        probe -= timedelta(days=1)
    while by_date.get(probe.isoformat(), 0) > 0:
        current += 1
        probe -= timedelta(days=1)

    longest = 0
    run = 0
    for d in sorted(by_date):
        if by_date[d] > 0:
            run += 1
            longest = max(longest, run)
        else:
            run = 0

    best = max(by_date.items(), key=lambda kv: (kv[1], -by_date[kv[0]])) if by_date else ("", 0)
    best_day = best[0] if best[1] > 0 else ""

    monthly = defaultdict(int)
    for d in days:
        monthly[d["date"][:7]] += d["level"]

    return {
        "total": total_levels,
        "current_streak": current,
        "longest_streak": longest,
        "best_day": best_day,
        "monthly": dict(sorted(monthly.items())),
    }


def parse_real(user: str) -> tuple[list[dict], int | None]:
    resp = requests.get(URL.format(user=user), headers=HEADERS, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    cells = soup.select("td[data-date][data-level]")
    if not cells:
        raise ValueError("no contribution cells found in HTML")

    days: list[dict] = []
    seen: set[str] = set()
    for cell in cells:
        date_str = cell.get("data-date", "")
        try:
            datetime.fromisoformat(date_str)
        except ValueError:
            continue
        if date_str in seen:
            continue
        seen.add(date_str)
        days.append({"date": date_str, "level": int(cell.get("data-level", "0"))})
    days.sort(key=lambda d: d["date"])

    match = re.search(r"([\d,]+)\s+contributions? in the last year", resp.text)
    total = int(match.group(1).replace(",", "")) if match else None
    return days, total


def generate_example() -> list[dict]:
    rng = random.Random(EXAMPLE_SEED)
    start = date.today() - timedelta(days=EXAMPLE_DAYS - 1)

    def level() -> int:
        r = rng.random()
        if r < 0.62:
            return 0
        if r < 0.80:
            return 1
        if r < 0.90:
            return 2
        if r < 0.97:
            return 3
        return 4

    days = []
    for offset in range(EXAMPLE_DAYS):
        day = start + timedelta(days=offset)
        days.append({"date": day.isoformat(), "level": level()})
    return days


def main() -> None:
    user = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_USER
    real_total: int | None = None
    used_fallback = False
    try:
        days, real_total = parse_real(user)
    except Exception as exc:  # network or parse failure -> deterministic example
        used_fallback = True
        print(
            f"warning: could not fetch real contributions for {user} "
            f"({exc}); wrote deterministic example data instead",
            file=sys.stderr,
        )
        days = generate_example()

    stats = compute_stats(days)
    if real_total is not None:
        stats["total"] = real_total

    payload = {"username": user, "days": days, "stats": stats}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")

    source = "example" if used_fallback else "real"
    print(f"wrote {OUT} ({source}, {len(days)} days, total={stats['total']})")


if __name__ == "__main__":
    main()
