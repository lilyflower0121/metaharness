#!/usr/bin/env python3
"""Validate explicit scope-boundary declarations for metaharness contracts."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from yaml_compat import load_path

ROOT = Path(__file__).resolve().parents[1]
BAD = {"", "tbd", "todo", "unknown", "none", "n/a", "na", "null", "-"}

REQUIRED_TOP = [
    "in_scope",
    "out_of_scope",
    "cannot_harness",
    "boundary_assumptions",
    "accident_scenarios",
    "escalation_triggers",
]


def meaningful(v: Any) -> bool:
    if v is None:
        return False
    if isinstance(v, str):
        s = v.strip()
        return bool(s) and s.lower() not in BAD and len(s) >= 3
    if isinstance(v, list):
        return bool(v) and all(meaningful(i) for i in v)
    if isinstance(v, dict):
        return bool(v) and all(meaningful(i) for i in v.values())
    return True


def flatten(v: Any) -> str:
    if isinstance(v, dict):
        return " ".join(f"{k} {flatten(val)}" for k, val in v.items())
    if isinstance(v, list):
        return " ".join(flatten(i) for i in v)
    return "" if v is None else str(v)


def list_like(v: Any) -> bool:
    return isinstance(v, list) and meaningful(v)


def validate_cannot_harness(items: Any, errors: list[str]) -> None:
    if not isinstance(items, list) or not items:
        errors.append("scope_boundary.cannot_harness must be a non-empty list")
        return
    for i, item in enumerate(items):
        if isinstance(item, str):
            errors.append(f"scope_boundary.cannot_harness[{i}] must include item/reason/required_escalation, not a bare string")
            continue
        if not isinstance(item, dict):
            errors.append(f"scope_boundary.cannot_harness[{i}] must be a mapping")
            continue
        for key in ["item", "reason", "required_escalation"]:
            if not meaningful(item.get(key)):
                errors.append(f"scope_boundary.cannot_harness[{i}] missing meaningful {key}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate scope-boundary harness fields")
    ap.add_argument("--contract", type=Path, required=True)
    args = ap.parse_args()
    path = args.contract if args.contract.is_absolute() else ROOT / args.contract
    try:
        data = load_path(path)
    except Exception as exc:
        print(f"SCOPE BOUNDARY GATE FAIL: cannot read contract: {exc}")
        return 2
    errors: list[str] = []
    if not isinstance(data, dict):
        errors.append("contract root must be mapping")
        data = {}

    scope = data.get("scope_boundary")
    if not isinstance(scope, dict):
        errors.append("missing scope_boundary mapping")
        scope = {}

    for key in REQUIRED_TOP:
        if key == "cannot_harness":
            validate_cannot_harness(scope.get(key), errors)
        elif not list_like(scope.get(key)):
            errors.append(f"scope_boundary.{key} must be a non-empty list")

    out_text = flatten(scope.get("out_of_scope", "")).lower()
    cannot_text = flatten(scope.get("cannot_harness", "")).lower()
    if out_text and cannot_text and out_text == cannot_text:
        errors.append("out_of_scope and cannot_harness must not be identical; cannot_harness should name unverifiable claims/actions")

    risk = str(data.get("risk_tier", "")).lower()
    if risk in {"medium", "high"}:
        if not list_like(scope.get("accident_scenarios")):
            errors.append("medium/high contracts require scope_boundary.accident_scenarios")
        if not list_like(scope.get("escalation_triggers")):
            errors.append("medium/high contracts require scope_boundary.escalation_triggers")

    rel = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
    if errors:
        print(f"SCOPE BOUNDARY GATE FAIL: {rel}")
        for err in errors:
            print(f"- {err}")
        return 1
    print(f"SCOPE BOUNDARY GATE PASS: {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
