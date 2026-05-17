#!/usr/bin/env python3
"""Risk-tiered contract gate for metaharness.

This validator intentionally checks structural obligations, not task-specific truth.
It is designed to fail closed when risk-appropriate fields are missing so that
natural-language harness rules become enforceable before a task passes a gate.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from yaml_compat import load_path

RISK_ORDER = {"low": 1, "medium": 2, "high": 3}

BASE_REQUIRED = [
    "objective",
    "non_goals",
    "constraints.external_side_effect_policy",
    "evidence_policy.required_sources",
    "validation.success_criteria",
    "stop_conditions",
]

MEDIUM_REQUIRED = BASE_REQUIRED + [
    "prohibited_substitutions",
    "constraints.allowed_paths",
    "constraints.allowed_tools",
    "validation.validator_role",
    "rollback.rollback_path",
]

HIGH_REQUIRED = MEDIUM_REQUIRED + [
    "constraints.data_classification",
    "authority.requested_by",
    "authority.approved_actions",
    "authority.ambiguous_scope_owner",
]


def load_yaml(path: Path) -> dict[str, Any]:
    data = load_path(path)
    if not isinstance(data, dict):
        raise ValueError("contract root must be a mapping")
    return data


def get_path(data: dict[str, Any], dotted: str) -> Any:
    cur: Any = data
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def present(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, set, dict)):
        return bool(value)
    return True


def require_fields(data: dict[str, Any], fields: list[str], errors: list[str]) -> None:
    for field in fields:
        if not present(get_path(data, field)):
            errors.append(f"missing required field: {field}")


def risk_required_fields(risk: str) -> list[str]:
    if risk == "low":
        return BASE_REQUIRED
    if risk == "medium":
        return MEDIUM_REQUIRED
    if risk == "high":
        return HIGH_REQUIRED
    raise ValueError(f"unknown risk: {risk}")


def validate(data: dict[str, Any], expected_risk: str) -> list[str]:
    errors: list[str] = []
    declared = data.get("risk_tier")
    if declared not in RISK_ORDER:
        errors.append("risk_tier must be one of: low, medium, high")
    elif declared != expected_risk:
        errors.append(f"risk_tier mismatch: contract declares {declared!r}, gate expected {expected_risk!r}")

    require_fields(data, risk_required_fields(expected_risk), errors)

    side_effect_policy = get_path(data, "constraints.external_side_effect_policy")
    if expected_risk == "low" and str(side_effect_policy).strip().lower() not in {"none", "no external side effects", "read-only"}:
        errors.append("low-risk contracts must declare constraints.external_side_effect_policy as none/read-only")

    if expected_risk in {"medium", "high"}:
        automated = get_path(data, "validation.automated_checks")
        manual = get_path(data, "validation.manual_checks")
        if not present(automated) and not present(manual):
            errors.append("medium/high contracts require validation.automated_checks or validation.manual_checks")

    if expected_risk == "high":
        approved = get_path(data, "authority.approved_actions")
        if isinstance(approved, list) and any(str(x).strip().lower() in {"*", "all", "anything"} for x in approved):
            errors.append("high-risk authority.approved_actions must not be wildcard/all")
        rollback = get_path(data, "rollback.rollback_path")
        irreversible = get_path(data, "rollback.irreversible_actions")
        if not present(rollback) and not present(irreversible):
            errors.append("high-risk contracts require rollback.rollback_path or rollback.irreversible_actions")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a metaharness contract against a risk-tier gate.")
    parser.add_argument("--risk", choices=sorted(RISK_ORDER), required=True)
    parser.add_argument("--contract", type=Path, required=True)
    args = parser.parse_args()

    try:
        data = load_yaml(args.contract)
    except Exception as exc:
        print(f"GATE FAIL: could not read contract: {exc}", file=sys.stderr)
        return 2

    errors = validate(data, args.risk)
    if errors:
        print(f"GATE FAIL: {args.contract} did not satisfy {args.risk} risk requirements")
        for err in errors:
            print(f"- {err}")
        return 1

    print(f"GATE PASS: {args.contract} satisfies {args.risk} risk requirements")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
