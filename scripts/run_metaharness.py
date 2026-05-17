#!/usr/bin/env python3
"""Run the shared metaharness gate suite for a contract.

This is the stable entrypoint for Claude Code, Codex, Hermes Agent, and other
agent runtimes. It composes lower-level validators and emits a compact receipt.
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path
from yaml_compat import load_path

ROOT = Path(__file__).resolve().parents[1]

def has_section(data: dict, key: str) -> bool:
    return isinstance(data.get(key), dict) and bool(data[key])

def run(cmd: list[str]) -> dict:
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    return {
        "command": cmd,
        "exit_code": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "status": "pass" if proc.returncode == 0 else "fail",
    }

def main() -> int:
    ap = argparse.ArgumentParser(description="Run metaharness validator suite.")
    ap.add_argument("--contract", type=Path, required=True)
    ap.add_argument("--json", action="store_true", help="Emit JSON receipt only")
    args = ap.parse_args()

    contract = args.contract if args.contract.is_absolute() else ROOT / args.contract
    try:
        data = load_path(contract)
    except Exception as exc:
        print(f"METAHARNESS SUITE FAIL: cannot read contract: {exc}", file=sys.stderr)
        return 2
    if not isinstance(data, dict):
        print("METAHARNESS SUITE FAIL: contract root must be mapping", file=sys.stderr)
        return 2
    risk = data.get("risk_tier")
    if risk not in {"low", "medium", "high"}:
        print("METAHARNESS SUITE FAIL: risk_tier must be low, medium, or high", file=sys.stderr)
        return 2

    rel = str(contract.relative_to(ROOT)) if contract.is_relative_to(ROOT) else str(contract)
    commands = [
        [sys.executable, "scripts/metaharness_gate.py", "--risk", risk, "--contract", rel],
        [sys.executable, "scripts/phase_risk_gate.py", "--contract", rel],
    ]
    if has_section(data, "artifact_flow"):
        commands.append([sys.executable, "scripts/artifact_flow_gate.py", "--contract", rel])

    results = [run(cmd) for cmd in commands]
    ok = all(r["exit_code"] == 0 for r in results)
    receipt = {
        "schema": "metaharness.gate_receipt.v0",
        "contract": rel,
        "risk_tier": risk,
        "phase": data.get("phase"),
        "status": "pass" if ok else "fail",
        "validators": results,
    }
    if args.json:
        print(json.dumps(receipt, indent=2))
    else:
        print(f"METAHARNESS SUITE {'PASS' if ok else 'FAIL'}: {rel} ({data.get('phase')}/{risk})")
        for r in results:
            print(f"- {r['status'].upper()}: {' '.join(r['command'])}")
            if r['stdout']:
                print("  stdout:", r['stdout'].replace("\n", "\n          "))
            if r['stderr']:
                print("  stderr:", r['stderr'].replace("\n", "\n          "))
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
