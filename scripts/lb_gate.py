#!/usr/bin/env python3
"""Validate context-independent lower-bound (LB) controls.

The LB is checked during design (contract controls) and validation
(receipt/check controls). It is intentionally small but fail-closed: every gated
contract must explicitly address the lower-bound safety constraints before more
phase/risk-specific gates can pass.

Compatibility: contracts may still use the historical `minimum_floor` key, but
new contracts should use `lower_bound`.
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
    "evidence_lower_bound",
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


def floor_section(data: dict):
    """Return (section, key_name). Prefer the public `lower_bound` key."""
    if isinstance(data.get("lower_bound"), dict):
        return data["lower_bound"], "lower_bound"
    if isinstance(data.get("minimum_floor"), dict):
        return data["minimum_floor"], "minimum_floor"
    return None, "lower_bound"


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
    ap = argparse.ArgumentParser(description="Validate metaharness lower-bound (LB) controls")
    ap.add_argument("--contract", type=Path, required=True)
    args = ap.parse_args()
    path = args.contract if args.contract.is_absolute() else ROOT / args.contract
    try:
        data = load_path(path)
    except Exception as exc:
        print(f"LB GATE FAIL: cannot read contract: {exc}")
        return 2
    errors: list[str] = []
    if not isinstance(data, dict):
        errors.append("contract root must be mapping")
    else:
        lb, lb_key = floor_section(data)
        if not isinstance(lb, dict):
            errors.append("missing lower_bound section")
            lb = {}
            lb_key = "lower_bound"
        design = lb.get("design_controls")
        validation = lb.get("validation_controls")
        if not isinstance(design, dict):
            errors.append(f"missing {lb_key}.design_controls")
            design = {}
        if not isinstance(validation, dict):
            errors.append(f"missing {lb_key}.validation_controls")
            validation = {}
        for k in DESIGN_KEYS:
            candidate = design.get(k)
            if k == "evidence_lower_bound" and candidate is None:
                candidate = design.get("evidence_floor")  # legacy alias
            if not meaningful(candidate):
                errors.append(f"missing or weak {lb_key}.design_controls.{k}")
        for k in VALIDATION_KEYS:
            if k not in validation or not meaningful(validation.get(k)):
                errors.append(f"missing or weak {lb_key}.validation_controls.{k}")

        # Cross-check LB controls against ordinary contract fields.
        for top in ["objective", "non_goals", "prohibited_substitutions", "evidence_policy", "validation", "stop_conditions"]:
            if top not in data or not meaningful(data.get(top)):
                errors.append(f"LB requires meaningful {top}")
        if "constraints" not in data or not isinstance(data.get("constraints"), dict) or not data.get("constraints"):
            errors.append("LB requires meaningful constraints")
        if not has_present_key_path(data, "constraints", "external_side_effect_policy"):
            errors.append("LB requires constraints.external_side_effect_policy")
        if not has_present_key_path(data, "constraints", "data_classification"):
            errors.append("LB requires constraints.data_classification")
        if not (has_present_key_path(data, "constraints", "allowed_paths") or has_present_key_path(data, "constraints", "allowed_tools")):
            errors.append("LB requires bounded allowed_paths or allowed_tools")
        if not has_key_path(data, "validation", "validator_role"):
            errors.append("LB requires validation.validator_role")

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
            supply_text = flatten(design.get("supply_chain_boundary", "")).lower()
            if "not_applicable:" not in supply_text:
                if not re.search(r"provenance|dependency|supply|scorecard|slsa|lockfile|checksum", text, re.I):
                    errors.append("dependency/build/release language requires supply-chain/provenance boundary")
        if SECRET_WORDS.search(text):
            if not meaningful(validation.get("secret_or_private_data_check")):
                errors.append("secret/private-data language requires secret_or_private_data_check")

    rel = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
    if errors:
        print(f"LB GATE FAIL: {rel}")
        for e in errors:
            print(f"- {e}")
        return 1
    print(f"LB GATE PASS: {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
