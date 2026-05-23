#!/usr/bin/env python3
"""Validate explicit coverage-boundary declarations for metaharness contracts."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from yaml_compat import load_path

ROOT = Path(__file__).resolve().parents[1]
BAD = {"", "tbd", "todo", "unknown", "none", "n/a", "na", "null", "-"}
STATUS_DECLARED = {"pass", "fail", "blocked"}
STATUS_DOMAIN = {"pass", "fail", "not_assessed", "blocked"}
STATUS_SERVICE = {"pass", "fail", "not_assessed", "blocked"}


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


def non_empty_list(v: Any) -> bool:
    return isinstance(v, list) and meaningful(v)


def as_status(section: dict[str, Any], path: str, allowed: set[str], errors: list[str]) -> str:
    status = str(section.get("status", "")).strip().lower()
    if status not in allowed:
        errors.append(f"{path}.status must be one of {sorted(allowed)}")
    return status


def validate_denominator(boundary: dict[str, Any], errors: list[str]) -> None:
    denom = boundary.get("denominator")
    if not isinstance(denom, dict):
        errors.append("coverage_boundary.denominator must be a mapping")
        return
    for key in ["id", "description", "includes", "excludes"]:
        if not meaningful(denom.get(key)):
            errors.append(f"coverage_boundary.denominator missing meaningful {key}")
    if not non_empty_list(denom.get("includes")):
        errors.append("coverage_boundary.denominator.includes must be a non-empty list")
    if not non_empty_list(denom.get("excludes")):
        errors.append("coverage_boundary.denominator.excludes must be a non-empty list")


def validate_declared_scope(boundary: dict[str, Any], errors: list[str]) -> None:
    section = boundary.get("declared_scope_coverage")
    if not isinstance(section, dict):
        errors.append("coverage_boundary.declared_scope_coverage must be a mapping")
        return
    status = as_status(section, "coverage_boundary.declared_scope_coverage", STATUS_DECLARED, errors)
    if status == "pass":
        denom = boundary.get("denominator")
        denom_id = denom.get("id") if isinstance(denom, dict) else None
        if not meaningful(denom_id):
            errors.append("declared_scope_coverage.status=pass requires coverage_boundary.denominator.id")
        if not meaningful(section.get("denominator")):
            errors.append("declared_scope_coverage.status=pass requires declared_scope_coverage.denominator")
        elif meaningful(denom_id) and str(section.get("denominator")) != str(denom_id):
            errors.append("declared_scope_coverage.denominator must match coverage_boundary.denominator.id")
        blockers = section.get("missing_blockers")
        if blockers not in ([], None):
            errors.append("declared_scope_coverage.status=pass requires missing_blockers to be empty")
        if not meaningful(section.get("meaning")):
            errors.append("declared_scope_coverage.status=pass requires a scoped meaning statement")


def validate_domain_and_service(boundary: dict[str, Any], errors: list[str]) -> None:
    domain = boundary.get("domain_coverage_completeness")
    if not isinstance(domain, dict):
        errors.append("coverage_boundary.domain_coverage_completeness must be a mapping")
    else:
        status = as_status(domain, "coverage_boundary.domain_coverage_completeness", STATUS_DOMAIN, errors)
        if status in {"not_assessed", "fail", "blocked"} and not meaningful(domain.get("reason")):
            errors.append("domain_coverage_completeness non-pass status requires reason")

    service = boundary.get("service_use_coverage")
    if not isinstance(service, dict):
        errors.append("coverage_boundary.service_use_coverage must be a mapping")
        return
    status = as_status(service, "coverage_boundary.service_use_coverage", STATUS_SERVICE, errors)
    blockers = service.get("blockers", [])
    if status == "pass" and meaningful(blockers):
        errors.append("service_use_coverage.status=pass is incompatible with service blockers")
    if status in {"not_assessed", "fail", "blocked"} and not meaningful(service.get("reason")):
        errors.append("service_use_coverage non-pass status requires reason")


def validate_out_of_scope_blockers(boundary: dict[str, Any], errors: list[str]) -> None:
    items = boundary.get("out_of_scope_blockers")
    if not isinstance(items, list):
        errors.append("coverage_boundary.out_of_scope_blockers must be a list")
        return
    service = boundary.get("service_use_coverage")
    service_status = str(service.get("status", "")).lower() if isinstance(service, dict) else ""
    blocking_items = []
    for i, item in enumerate(items):
        if isinstance(item, str):
            errors.append(f"coverage_boundary.out_of_scope_blockers[{i}] must be structured, not a bare string")
            continue
        if not isinstance(item, dict):
            errors.append(f"coverage_boundary.out_of_scope_blockers[{i}] must be a mapping")
            continue
        for key in ["item", "reason", "required_escalation"]:
            if not meaningful(item.get(key)):
                errors.append(f"coverage_boundary.out_of_scope_blockers[{i}] missing meaningful {key}")
        if item.get("blocks_service_use") is True:
            blocking_items.append(i)
        for key in ["acceptable_for_declared_scope", "blocks_domain_claim", "blocks_service_use"]:
            if key in item and not isinstance(item.get(key), bool):
                errors.append(f"coverage_boundary.out_of_scope_blockers[{i}].{key} must be boolean when present")
    if service_status == "pass" and blocking_items:
        errors.append("service_use_coverage.status=pass is incompatible with out_of_scope_blockers that block service use")


def validate_claims(boundary: dict[str, Any], data: dict[str, Any], errors: list[str]) -> None:
    if not non_empty_list(boundary.get("allowed_claims")):
        errors.append("coverage_boundary.allowed_claims must be a non-empty list")
    if not non_empty_list(boundary.get("forbidden_claims")):
        errors.append("coverage_boundary.forbidden_claims must be a non-empty list")
    if str(data.get("critical_coverage", "")).strip().lower() == "pass":
        errors.append("top-level critical_coverage: pass is denominator-free; use coverage_boundary.declared_scope_coverage instead")
    allowed_text = " ".join(str(x).lower() for x in boundary.get("allowed_claims", []))
    if "denominator" not in allowed_text and "scope" not in allowed_text:
        errors.append("allowed_claims must state that coverage is denominator- or scope-limited")


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate coverage-boundary harness fields")
    ap.add_argument("--contract", type=Path, required=True)
    args = ap.parse_args()
    path = args.contract if args.contract.is_absolute() else ROOT / args.contract
    try:
        data = load_path(path)
    except Exception as exc:
        print(f"COVERAGE BOUNDARY GATE FAIL: cannot read contract: {exc}")
        return 2
    errors: list[str] = []
    if not isinstance(data, dict):
        errors.append("contract root must be mapping")
        data = {}

    boundary = data.get("coverage_boundary")
    if not isinstance(boundary, dict):
        errors.append("missing coverage_boundary mapping")
        boundary = {}

    validate_denominator(boundary, errors)
    validate_declared_scope(boundary, errors)
    validate_domain_and_service(boundary, errors)
    validate_out_of_scope_blockers(boundary, errors)
    validate_claims(boundary, data, errors)

    rel = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
    if errors:
        print(f"COVERAGE BOUNDARY GATE FAIL: {rel}")
        for err in errors:
            print(f"- {err}")
        return 1
    print(f"COVERAGE BOUNDARY GATE PASS: {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
