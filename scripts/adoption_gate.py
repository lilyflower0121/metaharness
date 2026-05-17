#!/usr/bin/env python3
"""Validate metaharness adoption packets.

This gate is intentionally structural and adoption-focused. It ensures target
repositories do not accidentally treat the shared metaharness repository as a
wholesale vendored dependency and that copied artifacts have local ownership and
verification.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from yaml_compat import load_path

ROOT = Path(__file__).resolve().parents[1]
CLASSES = {
    "copy_as_is",
    "copy_then_configure",
    "adapt_policy",
    "interpret_pattern",
    "reference_only",
}
COPY_CLASSES = {"copy_as_is", "copy_then_configure"}
BAD = {"", "tbd", "todo", "unknown", "none", "n/a", "na", "null", "-"}


def meaningful(value: Any) -> bool:
    if isinstance(value, str):
        return value.strip().lower() not in BAD
    if isinstance(value, list):
        return bool(value) and all(meaningful(v) for v in value)
    if isinstance(value, dict):
        return bool(value)
    return value is not None


def flatten(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(f"{k} {flatten(v)}" for k, v in value.items())
    if isinstance(value, list):
        return " ".join(flatten(v) for v in value)
    return "" if value is None else str(value)


def as_list(value: Any, path: str, errors: list[str]) -> list[Any]:
    if not isinstance(value, list):
        errors.append(f"{path} must be a list")
        return []
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate metaharness adoption packet")
    parser.add_argument("--contract", "--packet", dest="contract", type=Path, required=True)
    args = parser.parse_args()
    path = args.contract if args.contract.is_absolute() else ROOT / args.contract
    try:
        data = load_path(path)
    except Exception as exc:
        print(f"ADOPTION GATE FAIL: cannot read contract: {exc}")
        return 2

    errors: list[str] = []
    if not isinstance(data, dict):
        errors.append("contract root must be mapping")
        adoption = {}
    else:
        adoption = data.get("metaharness_adoption")
        if not isinstance(adoption, dict):
            errors.append("missing metaharness_adoption mapping")
            adoption = {}

    for key in ["source_version", "target_repo", "adoption_goal", "local_policy_sources", "validators", "update_policy"]:
        if not meaningful(adoption.get(key)):
            errors.append(f"missing or weak metaharness_adoption.{key}")

    adopted = as_list(adoption.get("adopted"), "metaharness_adoption.adopted", errors)
    if not adopted:
        errors.append("metaharness_adoption.adopted must contain at least one decision")
    for i, item in enumerate(adopted):
        p = f"metaharness_adoption.adopted[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{p} must be mapping")
            continue
        for key in ["source", "class", "target", "local_decision"]:
            if not meaningful(item.get(key)):
                errors.append(f"missing or weak {p}.{key}")
        cls = item.get("class")
        if cls not in CLASSES:
            errors.append(f"{p}.class must be one of: {', '.join(sorted(CLASSES))}")
        if cls in COPY_CLASSES:
            for key in ["local_owner", "verification"]:
                if not meaningful(item.get(key)):
                    errors.append(f"{p}.{key} is required for {cls}")
        text = flatten(item).lower()
        if cls in COPY_CLASSES and "full metaharness" in text:
            errors.append(f"{p} must not copy/vendor the full metaharness repository")
        if cls == "reference_only" and meaningful(item.get("verification")):
            # Reference-only can have a citation/readback, but should not pretend to run a copied artifact.
            verification = flatten(item.get("verification")).lower()
            if any(word in verification for word in ["copied", "copy", "installed", "vendored"]):
                errors.append(f"{p}.verification conflicts with reference_only classification")

    skipped = adoption.get("skipped", [])
    if skipped is None:
        skipped = []
    for i, item in enumerate(as_list(skipped, "metaharness_adoption.skipped", errors)):
        p = f"metaharness_adoption.skipped[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{p} must be mapping")
            continue
        for key in ["source", "reason"]:
            if not meaningful(item.get(key)):
                errors.append(f"missing or weak {p}.{key}")

    policy_sources = adoption.get("local_policy_sources")
    validators = adoption.get("validators")
    if isinstance(policy_sources, list) and len(policy_sources) != len(set(map(str, policy_sources))):
        errors.append("metaharness_adoption.local_policy_sources contains duplicates")
    if isinstance(validators, list) and not any("run_metaharness.py" in str(v) or "gate" in str(v).lower() for v in validators):
        errors.append("metaharness_adoption.validators should name at least one gate or run_metaharness command")

    rel = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
    if errors:
        print(f"ADOPTION GATE FAIL: {rel}")
        for e in errors:
            print(f"- {e}")
        return 1
    print(f"ADOPTION GATE PASS: {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
