#!/usr/bin/env python3
"""Run the low-risk-readonly-harness risk-tier gate from inside this skill directory."""
from __future__ import annotations
import argparse, subprocess, sys
from pathlib import Path

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--contract', required=True)
    ns=ap.parse_args()
    root=Path(__file__).resolve().parents[3]
    cmd=[sys.executable, str(root/'scripts'/'metaharness_gate.py'), '--risk', 'low', '--contract', ns.contract]
    return subprocess.call(cmd, cwd=root)
if __name__=='__main__':
    raise SystemExit(main())
