#!/usr/bin/env python3
"""Validate common artifact-construction flow fields in a metaharness contract."""
from __future__ import annotations
import argparse, sys
from pathlib import Path
from typing import Any
from yaml_compat import load_path

REQUIRED = ['artifact_type', 'target_users', 'deliverables', 'build_steps', 'validators', 'acceptance_receipt']

def present(v: Any) -> bool:
    if v is None: return False
    if isinstance(v, str): return bool(v.strip()) and v.strip().upper() != 'TBD'
    if isinstance(v, (list, tuple, set)):
        return bool(v) and not all(str(x).strip().upper() == 'TBD' for x in v)
    if isinstance(v, dict): return bool(v)
    return True

def main() -> int:
    ap = argparse.ArgumentParser(description='Validate artifact_flow contract section.')
    ap.add_argument('--contract', type=Path, required=True)
    ns = ap.parse_args()
    try:
        data = load_path(ns.contract)
    except Exception as exc:
        print(f'ARTIFACT GATE FAIL: could not read contract: {exc}')
        return 2
    if not isinstance(data, dict):
        print('ARTIFACT GATE FAIL: contract root must be a mapping')
        return 2
    flow = data.get('artifact_flow')
    errors=[]
    if not isinstance(flow, dict):
        errors.append('missing artifact_flow mapping')
    else:
        for k in REQUIRED:
            if not present(flow.get(k)):
                errors.append(f'missing or TBD artifact_flow.{k}')
        vals = flow.get('validators')
        if isinstance(vals, list) and not any('metaharness_gate.py' in str(v) for v in vals):
            errors.append('artifact_flow.validators should include risk-tier gate or point to a validator suite including it')
    if errors:
        print(f'ARTIFACT GATE FAIL: {ns.contract}')
        for e in errors: print(f'- {e}')
        return 1
    print(f'ARTIFACT GATE PASS: {ns.contract}')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
