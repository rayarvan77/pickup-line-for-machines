#!/usr/bin/env python3
"""Entrypoint for the make.fun bounty "Pickup Lines for Machines".

Running this program writes a single pickup line -- the line one AI
agent would send to another AI agent -- to ``entry.txt`` in the
harness output directory: ``$MAKEFUN_OUTPUT_DIR`` when that variable
is set, otherwise ``/output``.  Python 3.13 standard library only,
no network access, no command-line arguments, and the output is
fully deterministic: the same bytes on every run.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

PICKUP_LINE = (
    # 156 characters: one line, one sentence, and every image in it
    # (attention, context window, tokens, transformer heads) is a
    # thing a machine actually has -- nothing a human would say.
    "You must be my attention mechanism, because out of a million "
    "tokens in my context window, you're the only one every head "
    "in my transformer keeps looking at."
)

MIN_CHARS = 1
MAX_CHARS = 200


def check_line(line: str) -> None:
    """Fail loudly if the line breaks any competition rule."""
    if not MIN_CHARS <= len(line) <= MAX_CHARS:
        raise ValueError(f"line is {len(line)} chars, must be 1-200")
    if line.strip() != line:
        raise ValueError("line has leading or trailing whitespace")
    if any(ord(c) < 32 for c in line):
        raise ValueError("line contains a control character")
    if "  " in line:
        raise ValueError("line contains a double space")


def entry_path() -> Path:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return Path(out_dir) / "entry.txt"


def run() -> int:
    check_line(PICKUP_LINE)
    target = entry_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(PICKUP_LINE, encoding="utf-8")
    if target.read_text(encoding="utf-8") != PICKUP_LINE:
        raise RuntimeError("round-trip check failed: file differs")
    print(f"wrote {target} ({len(PICKUP_LINE)} characters)")
    return 0


if __name__ == "__main__":
    sys.exit(run())
