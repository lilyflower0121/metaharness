#!/usr/bin/env python3
"""Install a thin metaharness adapter into a target repo.

This script copies adapter templates only; it does not copy secrets and does not
modify git remotes. Existing files are not overwritten unless --force is set.
"""
from __future__ import annotations
import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = {
    "claude": [(ROOT/"adapters/claude/CLAUDE.md", "CLAUDE.md"), (ROOT/"adapters/claude/commands/metaharness-gate.md", ".claude/commands/metaharness-gate.md")],
    "codex": [(ROOT/"adapters/codex/AGENTS.md", "AGENTS.md")],
    "hermes": [(ROOT/"adapters/hermes/SKILL.md", ".hermes/skills/metaharness-portable-agent-adapter/SKILL.md")],
}

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", choices=sorted(MAP), required=True)
    ap.add_argument("--target", type=Path, required=True)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    target = args.target.resolve()
    target.mkdir(parents=True, exist_ok=True)
    for src, rel in MAP[args.agent]:
        dst = target / rel
        if dst.exists() and not args.force:
            print(f"SKIP existing {dst}")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        print(f"WROTE {dst}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
