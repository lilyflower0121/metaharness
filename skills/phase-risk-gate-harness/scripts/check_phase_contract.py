#!/usr/bin/env python3
"""Run the root phase-risk gate from inside this skill directory."""
from __future__ import annotations
import argparse, subprocess, sys
from pathlib import Path

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--contract', required=True)
    ns=ap.parse_args()
    root=Path(__file__).resolve().parents[3]
    return subprocess.call([sys.executable, str(root/'scripts'/'phase_risk_gate.py'), '--contract', ns.contract], cwd=root)
if __name__=='__main__':
    raise SystemExit(main())
