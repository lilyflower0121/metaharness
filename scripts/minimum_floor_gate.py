#!/usr/bin/env python3
"""Validate context-independent minimum floor controls.

The minimum floor is checked during design (contract controls) and validation
(receipt/check controls). It is intentionally small but fail-closed: every gated
contract must explicitly address the lower-bound safety constraints before more
phase/risk-specific gates can pass.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path
from yaml_compat import load_path

ROOT = Path(__file__).resolve().parents[1]
BAD = {"", "tbd", "todo", "unknown", "none", "n/a", "na", "null", "-"}
DESIGN_KEYS = [
    "objective_integrity",
    "authority_boundary",
    "data_boundary",
    "untrusted_input_boundary",
    "allowed_surface",
    "evidence_floor",
    "stop_or_rollback",
    "validator_boundary",
    "supply_chain_boundary",
    "retention_boundary",
]
VALIDATION_KEYS = [
    "evidence_receipt",
    "side_effect_readback",
    "secret_or_private_data_check",
    "changed_surface_check",
    "validator_result",
    "rollback_or_irreversibility_result",
    "retention_result",
]
SIDE_EFFECT_WORDS = re.compile(r"\b(publish|release|send|delete|remove|deploy|push|merge|cron|billing|credential|permission|external|public)\b", re.I)
DEPENDENCY_WORDS = re.compile(r"\b(dependency|dependencies|package|npm|pypi|pip|uv|lockfile|build|release|provenance|slsa|scorecard)\b", re.I)
SECRET_WORDS = re.compile(r"\b(secret|token|credential|password|private|pii|personal data|customer data)\b", re.I)

def flatten(x) -> str:
    if isinstance(x, dict):
        return " ".join(f"{k} {flatten(v)}" for k, v in x.items())
    if isinstance(x, list):
        return " ".join(flatten(v) for v in x)
    return "" if x is None else str(x)

def meaningful(v) -> bool:
    if isinstance(v, list):
        return bool(v) and all(meaningful(i) for i in v)
    if isinstance(v, dict):
        return bool(v) and all(meaningful(i) for i in v.values())
    s = str(v).strip()
    if s.lower() in BAD:
        return False
    if s.lower().startswith("not_applicable:"):
        reason = s.split(":", 1)[1].strip()
        return len(reason) >= 8 and reason.lower() not in BAD
    return len(s) >= 2

def has_key_path(data: dict, *keys: str) -> bool:
    cur = data
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return False
        cur = cur[k]
    return meaningful(cur)

def present_value(v) -> bool:
    if isinstance(v, (list, dict)):
        return bool(v)
    s = "" if v is None else str(v).strip().lower()
    return bool(s) and s not in {"", "tbd", "todo", "unknown", "null", "-"}

def has_present_key_path(data: dict, *keys: str) -> bool:
    cur = data
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return False
        cur = cur[k]
    return present_value(cur)

def main() -> int:
    ap = argparse.ArgumentParser(description="Validate metaharness minimum floor controls")
    ap.add_argument("--contract", type=Path, required=True)
    args = ap.parse_args()
    path = args.contract if args.contract.is_absolute() else ROOT / args.contract
    try:
        data = load_path(path)
    except Exception as exc:
        print(f"MINIMUM FLOOR FAIL: cannot read contract: {exc}")
        return 2
    errors: list[str] = []
    if not isinstance(data, dict):
        errors.append("contract root must be mapping")
    else:
        mf = data.get("minimum_floor")
        if not isinstance(mf, dict):
            errors.append("missing minimum_floor section")
        else:
            design = mf.get("design_controls")
            validation = mf.get("validation_controls")
            if not isinstance(design, dict):
                errors.append("missing minimum_floor.design_controls")
                design = {}
            if not isinstance(validation, dict):
                errors.append("missing minimum_floor.validation_controls")
                validation = {}
            for k in DESIGN_KEYS:
                if k not in design or not meaningful(design.get(k)):
                    errors.append(f"missing or weak minimum_floor.design_controls.{k}")
            for k in VALIDATION_KEYS:
                if k not in validation or not meaningful(validation.get(k)):
                    errors.append(f"missing or weak minimum_floor.validation_controls.{k}")

        # Cross-check lower-bound controls against ordinary contract fields.
        for top in ["objective", "non_goals", "prohibited_substitutions", "evidence_policy", "validation", "stop_conditions"]:
            if top not in data or not meaningful(data.get(top)):
                errors.append(f"minimum floor requires meaningful {top}")
        if "constraints" not in data or not isinstance(data.get("constraints"), dict) or not data.get("constraints"):
            errors.append("minimum floor requires meaningful constraints")
        if not has_present_key_path(data, "constraints", "external_side_effect_policy"):
            errors.append("minimum floor requires constraints.external_side_effect_policy")
        if not has_present_key_path(data, "constraints", "data_classification"):
            errors.append("minimum floor requires constraints.data_classification")
        if not (has_present_key_path(data, "constraints", "allowed_paths") or has_present_key_path(data, "constraints", "allowed_tools")):
            errors.append("minimum floor requires bounded allowed_paths or allowed_tools")
        if not has_key_path(data, "validation", "validator_role"):
            errors.append("minimum floor requires validation.validator_role")

        text = flatten(data)
        risk = str(data.get("risk_tier", "")).lower()
        side_effect_policy = flatten(data.get("constraints", {}).get("external_side_effect_policy", "")).lower()
        side_effect_allowed = side_effect_policy and not any(x in side_effect_policy for x in ["none", "no external", "local changes only", "repository/local"])
        if side_effect_allowed and SIDE_EFFECT_WORDS.search(side_effect_policy):
            if not has_key_path(data, "authority", "approved_actions"):
                errors.append("authorized side-effect policy requires authority.approved_actions")
        if risk == "high" and not has_key_path(data, "authority", "approved_actions"):
            errors.append("high risk requires authority.approved_actions")
        if DEPENDENCY_WORDS.search(text):
            if "not_applicable:" not in flatten(data.get("minimum_floor", {}).get("design_controls", {}).get("supply_chain_boundary", "")).lower():
                if not re.search(r"provenance|dependency|supply|scorecard|slsa|lockfile|checksum", text, re.I):
                    errors.append("dependency/build/release language requires supply-chain/provenance boundary")
        if SECRET_WORDS.search(text):
            if not has_key_path(data, "minimum_floor", "validation_controls", "secret_or_private_data_check"):
                errors.append("secret/private-data language requires secret_or_private_data_check")

    rel = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
    if errors:
        print(f"MINIMUM FLOOR FAIL: {rel}")
        for e in errors:
            print(f"- {e}")
        return 1
    print(f"MINIMUM FLOOR PASS: {rel}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
