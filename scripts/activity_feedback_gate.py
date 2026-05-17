#!/usr/bin/env python3
"""Validate metaharness activity/feedback capture packets.

This gate checks the enforceable invariants in
``contracts/activity-feedback-capture.schema.yaml``.  It is intentionally small
and dependency-light so it can run in public repos without PyYAML; parsing goes
through ``scripts/yaml_compat.py``.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from yaml_compat import load_path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ID = "metaharness.activity_feedback_capture.v0"

RUN_REQUIRED = ["run_id", "task_contract_ref", "phase", "risk_tier", "actor_role", "runtime", "started_at", "status"]
PRIVACY_REQUIRED = [
    "data_classification",
    "raw_private_content_stored",
    "secrets_stored",
    "redaction_status",
    "evidence_access_model",
    "retention_ttl",
]
EVENT_REQUIRED = ["event_id", "timestamp", "actor_role", "event_type", "action_summary", "status", "raw_payload_stored"]
FEEDBACK_REQUIRED = ["feedback_id", "timestamp", "source_type", "authority", "summary", "disposition"]
DELTA_REQUIRED = ["delta_id", "source_feedback_ids", "classification", "statement", "status"]
PROMOTION_REQUIRED = ["promotion_id", "source_delta_ids", "target_type", "target_ref", "verification", "status"]

PHASES = {"exploration", "mvp_exploration", "specification", "implementation", "merge", "release", "operate", "retention"}
RISKS = {"low", "medium", "high"}
ACTOR_ROLES = {"intake", "planner", "executor", "tester", "validator", "curator", "tool", "human"}
EVENT_TYPES = {
    "plan_step", "tool_call", "artifact_read", "artifact_write", "command_run",
    "delegation", "validation", "feedback_review", "retention_decision", "stop", "rollback",
}
EVENT_STATUSES = {"started", "succeeded", "failed", "blocked", "skipped", "rolled_back"}
SOURCE_TYPES = {"human", "validator", "test", "runtime", "reviewer", "external_message", "model_inference"}
AUTHORITIES = {"instruction", "approval", "evidence_only", "weak_signal"}
DISPOSITIONS = {"unreviewed", "accepted", "rejected", "needs_clarification", "promoted", "discarded"}
DELTA_CLASSES = {
    "accepted_requirement", "bug", "ux_issue", "preference", "non_goal",
    "security_issue", "compliance_issue", "open_question", "rejected_inference",
}
DELTA_STATUSES = {"proposed", "accepted", "rejected", "deferred"}
PROMOTION_TARGETS = {"validator", "eval_case", "skill", "reference", "memory", "contract_update", "checklist", "discard"}
PROMOTION_STATUSES = {"proposed", "accepted", "rejected", "completed"}
REDACTION_STATUSES = {"not_needed", "pending", "redacted", "failed"}
DATA_CLASSES = {"public", "internal", "confidential", "restricted"}
ACCESS_MODELS = {"repository_inherited", "local_only", "restricted_artifact", "external_system"}
REVIEW_STATUSES = {"unreviewed", "reviewed", "blocked"}


def present(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, set, dict)):
        return bool(value)
    return True


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except Exception:
        return str(path)


def as_optional_list(value: Any, field: str, errors: list[str]) -> list[Any]:
    if value is None:
        return []
    if not isinstance(value, list):
        errors.append(f"invalid {field}: expected list")
        return []
    return value


def as_required_list(obj: dict[str, Any], key: str, field: str, errors: list[str]) -> list[Any]:
    value = obj.get(key)
    if not isinstance(value, list) or not value:
        errors.append(f"invalid {field}: expected non-empty list")
        return []
    return value


def require_mapping(data: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        errors.append(f"missing or invalid mapping: {key}")
        return {}
    return value


def require_list(data: dict[str, Any], key: str, errors: list[str]) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list):
        errors.append(f"missing or invalid list: {key}")
        return []
    if not value:
        errors.append(f"list must not be empty: {key}")
    return value


def require_fields(obj: dict[str, Any], fields: list[str], prefix: str, errors: list[str]) -> None:
    for field in fields:
        if not present(obj.get(field)) and obj.get(field) is not False:
            errors.append(f"missing required field: {prefix}.{field}")


def require_enum(value: Any, allowed: set[str], field: str, errors: list[str]) -> None:
    if value not in allowed:
        errors.append(f"invalid {field}: {value!r}; expected one of {', '.join(sorted(allowed))}")


def require_bool(value: Any, field: str, errors: list[str]) -> None:
    if not isinstance(value, bool):
        errors.append(f"invalid {field}: expected boolean")


def unique_id(items: list[Any], id_key: str, prefix: str, errors: list[str]) -> set[str]:
    ids: set[str] = set()
    for idx, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"{prefix}[{idx}] must be mapping")
            continue
        value = item.get(id_key)
        if not present(value):
            errors.append(f"missing {prefix}[{idx}].{id_key}")
            continue
        value = str(value)
        if value in ids:
            errors.append(f"duplicate {prefix}.{id_key}: {value}")
        ids.add(value)
    return ids


def validate_packet(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if data.get("schema") != SCHEMA_ID:
        errors.append(f"schema must be {SCHEMA_ID!r}")

    run = require_mapping(data, "run", errors)
    privacy = require_mapping(data, "privacy", errors)
    events = require_list(data, "events", errors)
    feedback = require_list(data, "feedback", errors)
    retention = require_mapping(data, "retention", errors)
    deltas = as_optional_list(data.get("requirement_deltas"), "requirement_deltas", errors)
    promotions = as_optional_list(data.get("promotions"), "promotions", errors)

    require_fields(run, RUN_REQUIRED, "run", errors)
    if run:
        require_enum(run.get("phase"), PHASES, "run.phase", errors)
        require_enum(run.get("risk_tier"), RISKS, "run.risk_tier", errors)
        require_enum(run.get("actor_role"), ACTOR_ROLES, "run.actor_role", errors)
        require_enum(run.get("status"), EVENT_STATUSES, "run.status", errors)

    require_fields(privacy, PRIVACY_REQUIRED, "privacy", errors)
    if privacy:
        require_enum(privacy.get("data_classification"), DATA_CLASSES, "privacy.data_classification", errors)
        require_enum(privacy.get("redaction_status"), REDACTION_STATUSES, "privacy.redaction_status", errors)
        require_enum(privacy.get("evidence_access_model"), ACCESS_MODELS, "privacy.evidence_access_model", errors)
        require_bool(privacy.get("raw_private_content_stored"), "privacy.raw_private_content_stored", errors)
        require_bool(privacy.get("secrets_stored"), "privacy.secrets_stored", errors)
        if privacy.get("data_classification") == "public" and privacy.get("raw_private_content_stored"):
            errors.append("public capture must not set privacy.raw_private_content_stored=true")
        if privacy.get("secrets_stored") and not (
            privacy.get("data_classification") == "restricted"
            and privacy.get("redaction_status") in {"redacted", "not_needed"}
        ):
            errors.append("privacy.secrets_stored=true requires restricted classification and redacted/not_needed status")
        if privacy.get("redaction_status") == "failed":
            errors.append("privacy.redaction_status=failed cannot pass gate")

    event_ids = unique_id(events, "event_id", "events", errors)
    for idx, event in enumerate(events):
        if not isinstance(event, dict):
            continue
        require_fields(event, EVENT_REQUIRED, f"events[{idx}]", errors)
        require_enum(event.get("actor_role"), ACTOR_ROLES, f"events[{idx}].actor_role", errors)
        require_enum(event.get("event_type"), EVENT_TYPES, f"events[{idx}].event_type", errors)
        require_enum(event.get("status"), EVENT_STATUSES, f"events[{idx}].status", errors)
        require_bool(event.get("raw_payload_stored"), f"events[{idx}].raw_payload_stored", errors)
        as_optional_list(event.get("evidence_refs"), f"events[{idx}].evidence_refs", errors)
        if privacy.get("data_classification") == "public" and event.get("raw_payload_stored"):
            errors.append(f"events[{idx}].raw_payload_stored must be false for public capture")

    feedback_ids = unique_id(feedback, "feedback_id", "feedback", errors)
    accepted_model_feedback: set[str] = set()
    for idx, item in enumerate(feedback):
        if not isinstance(item, dict):
            continue
        require_fields(item, FEEDBACK_REQUIRED, f"feedback[{idx}]", errors)
        require_enum(item.get("source_type"), SOURCE_TYPES, f"feedback[{idx}].source_type", errors)
        require_enum(item.get("authority"), AUTHORITIES, f"feedback[{idx}].authority", errors)
        require_enum(item.get("disposition"), DISPOSITIONS, f"feedback[{idx}].disposition", errors)
        related_event_ids = as_optional_list(item.get("related_event_ids"), f"feedback[{idx}].related_event_ids", errors)
        as_optional_list(item.get("evidence_refs"), f"feedback[{idx}].evidence_refs", errors)
        for event_id in related_event_ids:
            if event_id not in event_ids:
                errors.append(f"feedback[{idx}].related_event_ids references unknown event: {event_id}")
        if item.get("source_type") == "external_message" and item.get("authority") != "evidence_only":
            errors.append(f"feedback[{idx}] external_message must use authority=evidence_only unless separately contract-approved")
        if item.get("source_type") == "model_inference" and item.get("disposition") in {"accepted", "promoted"}:
            accepted_model_feedback.add(str(item.get("feedback_id")))

    delta_ids = unique_id(deltas, "delta_id", "requirement_deltas", errors)
    for idx, delta in enumerate(deltas):
        if not isinstance(delta, dict):
            errors.append(f"requirement_deltas[{idx}] must be mapping")
            continue
        require_fields(delta, DELTA_REQUIRED, f"requirement_deltas[{idx}]", errors)
        require_enum(delta.get("classification"), DELTA_CLASSES, f"requirement_deltas[{idx}].classification", errors)
        require_enum(delta.get("status"), DELTA_STATUSES, f"requirement_deltas[{idx}].status", errors)
        source_ids = [str(x) for x in as_required_list(delta, "source_feedback_ids", f"requirement_deltas[{idx}].source_feedback_ids", errors)]
        for feedback_id in source_ids:
            if feedback_id not in feedback_ids:
                errors.append(f"requirement_deltas[{idx}].source_feedback_ids references unknown feedback: {feedback_id}")
        if delta.get("status") == "accepted" and delta.get("classification") == "accepted_requirement":
            validator_refs = as_required_list(delta, "validator_refs", f"requirement_deltas[{idx}].validator_refs", errors)
            if any(fid in accepted_model_feedback for fid in source_ids):
                evidence_refs = {str(x) for x in as_optional_list(delta.get("evidence_refs"), f"requirement_deltas[{idx}].evidence_refs", errors)}
                if not ((evidence_refs & feedback_ids) - accepted_model_feedback):
                    errors.append(f"requirement_deltas[{idx}] model-inference requirement needs non-model confirmation evidence")

    unique_id(promotions, "promotion_id", "promotions", errors)
    for idx, promo in enumerate(promotions):
        if not isinstance(promo, dict):
            errors.append(f"promotions[{idx}] must be mapping")
            continue
        require_fields(promo, PROMOTION_REQUIRED, f"promotions[{idx}]", errors)
        require_enum(promo.get("target_type"), PROMOTION_TARGETS, f"promotions[{idx}].target_type", errors)
        require_enum(promo.get("status"), PROMOTION_STATUSES, f"promotions[{idx}].status", errors)
        source_delta_ids = as_required_list(promo, "source_delta_ids", f"promotions[{idx}].source_delta_ids", errors)
        for delta_id in source_delta_ids:
            if delta_id not in delta_ids:
                errors.append(f"promotions[{idx}].source_delta_ids references unknown delta: {delta_id}")
        if promo.get("status") in {"accepted", "completed"} and not present(promo.get("verification")):
            errors.append(f"promotions[{idx}] accepted/completed promotion requires verification")

    if retention:
        require_fields(retention, ["retention_reason", "review_status"], "retention", errors)
        as_required_list(retention, "keep_refs", "retention.keep_refs", errors)
        as_required_list(retention, "discard_refs", "retention.discard_refs", errors)
        require_enum(retention.get("review_status"), REVIEW_STATUSES, "retention.review_status", errors)
        if retention.get("review_status") != "reviewed":
            errors.append("retention.review_status must be reviewed before packet passes")

    return errors


def load_packet(path: Path) -> dict[str, Any]:
    data = load_path(path)
    if not isinstance(data, dict):
        raise ValueError("packet root must be mapping")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a metaharness activity/feedback capture packet.")
    parser.add_argument("--packet", type=Path, action="append", required=True, help="Packet YAML to validate; may be repeated.")
    args = parser.parse_args()

    any_errors = False
    for packet in args.packet:
        try:
            data = load_packet(packet)
        except Exception as exc:
            print(f"ACTIVITY FEEDBACK GATE FAIL: could not read {packet}: {exc}")
            any_errors = True
            continue
        errors = validate_packet(data)
        if errors:
            print(f"ACTIVITY FEEDBACK GATE FAIL: {packet}")
            for err in errors:
                print(f"- {err}")
            any_errors = True
        else:
            print(f"ACTIVITY FEEDBACK GATE PASS: {packet}")
    return 1 if any_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
