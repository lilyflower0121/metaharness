#!/usr/bin/env python3
"""Run the lower-bound (LB) gate for the given contract."""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

def main() -> int:
    contract = sys.argv[1] if len(sys.argv) > 1 else "contracts/examples/lower-bound.medium.valid.yaml"
    return subprocess.call([sys.executable, "scripts/lb_gate.py", "--contract", contract], cwd=ROOT)

if __name__ == "__main__":
    raise SystemExit(main())
