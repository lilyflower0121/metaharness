#!/usr/bin/env python3
"""Print a metaharness adapter template for a target runtime."""
from __future__ import annotations
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MAP = {
    "claude": ROOT / "adapters/claude/CLAUDE.md",
    "codex": ROOT / "adapters/codex/AGENTS.md",
    "hermes": ROOT / "adapters/hermes/SKILL.md",
}

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target", choices=sorted(MAP))
    args = ap.parse_args()
    print(MAP[args.target].read_text())
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
