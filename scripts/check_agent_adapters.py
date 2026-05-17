#!/usr/bin/env python3
"""Validate portable agent adapter files for Claude Code, Codex, and Hermes Agent."""
from __future__ import annotations
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "adapters/claude/CLAUDE.md": ["python3 scripts/run_metaharness.py --contract", "contract path", "risk tier", "phase"],
    "adapters/claude/commands/metaharness-gate.md": ["$ARGUMENTS", "run_metaharness.py"],
    "adapters/codex/AGENTS.md": ["python3 scripts/run_metaharness.py --contract", "Codex", "contract"],
    "adapters/hermes/SKILL.md": ["name: metaharness-portable-agent-adapter", "python3 scripts/run_metaharness.py --contract"],
    "skills/portable-agent-adapter-harness/SKILL.md": ["portable-agent-adapter-harness", "scripts/check_agent_adapters.py"],
}
FORBIDDEN = ["ANTHROPIC" + "_API_KEY", "OPENAI" + "_API_KEY", "password" + "=", "token" + "="]

def main() -> int:
    errors: list[str] = []
    for rel, needles in REQUIRED.items():
        p = ROOT / rel
        if not p.exists():
            errors.append(f"missing {rel}")
            continue
        text = p.read_text()
        for n in needles:
            if n not in text:
                errors.append(f"{rel} missing required text: {n}")
        for f in FORBIDDEN:
            if f.lower() in text.lower():
                errors.append(f"{rel} contains forbidden secret-like token: {f}")
    if errors:
        print("ADAPTER CHECK FAIL")
        for e in errors: print("-", e)
        return 1
    print("ADAPTER CHECK PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
