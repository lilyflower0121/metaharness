#!/usr/bin/env python3
"""Validate phase-specific gate requirements for metaharness contracts."""
from __future__ import annotations
import argparse, sys
from pathlib import Path
from typing import Any
from yaml_compat import load_path

PHASE_REQUIREMENTS = {
    'exploration': ['assumptions', 'evidence_sources'],
    'mvp_exploration': ['learning_goals', 'feedback_items', 'non_goal_checks'],
    'specification': ['requirement_validator_map'],
    'implementation': ['changed_surfaces', 'validators', 'rollback_path'],
    'merge': ['independent_validation', 'receipt_path', 'clean_status_check'],
    'release': ['authority', 'release_targets', 'readback_plan'],
    'operate': ['operation_stop_rules', 'monitoring', 'owner'],
    'retention': ['retention_decisions'],
}
HIGH_ESCALATOR_FIELDS = ['release_targets', 'authority']

def present(v: Any) -> bool:
    if v is None: return False
    if isinstance(v, str): return bool(v.strip()) and v.strip().upper() != 'TBD'
    if isinstance(v, (list, tuple, set)):
        return bool(v) and not all(str(x).strip().upper() == 'TBD' for x in v)
    if isinstance(v, dict): return bool(v)
    return True

def main() -> int:
    ap=argparse.ArgumentParser(description='Validate phase/risk gate fields.')
    ap.add_argument('--contract', type=Path, required=True)
    ns=ap.parse_args()
    try:
        data=load_path(ns.contract)
    except Exception as exc:
        print(f'PHASE GATE FAIL: could not read contract: {exc}')
        return 2
    if not isinstance(data, dict):
        print('PHASE GATE FAIL: contract root must be mapping'); return 2
    phase=data.get('phase')
    risk=data.get('risk_tier')
    errors=[]
    if phase not in PHASE_REQUIREMENTS:
        errors.append('phase must be one of: '+', '.join(PHASE_REQUIREMENTS))
    if risk not in {'low','medium','high'}:
        errors.append('risk_tier must be low, medium, or high')
    controls=data.get('phase_controls')
    if not isinstance(controls, dict):
        errors.append('missing phase_controls mapping')
        controls={}
    if phase in PHASE_REQUIREMENTS:
        for field in PHASE_REQUIREMENTS[phase]:
            if not present(controls.get(field)):
                errors.append(f'missing or TBD phase_controls.{field} for phase {phase}')
    if phase == 'mvp_exploration' and present(controls.get('release_targets')):
        errors.append('mvp_exploration must not declare release_targets; move to release phase')
    if phase in {'release','operate'} and risk != 'high':
        errors.append(f'{phase} phase requires risk_tier: high')
    if phase == 'release':
        if not present(controls.get('rollback_path')) and not present(controls.get('irreversible_actions')):
            errors.append('release phase requires phase_controls.rollback_path or irreversible_actions')
    if risk == 'low':
        for field in HIGH_ESCALATOR_FIELDS:
            if present(controls.get(field)):
                errors.append(f'low risk cannot include high-risk phase_controls.{field}')
    if errors:
        print(f'PHASE GATE FAIL: {ns.contract}')
        for e in errors: print('-', e)
        return 1
    print(f'PHASE GATE PASS: {ns.contract} ({phase}/{risk})')
    return 0
if __name__=='__main__':
    raise SystemExit(main())
