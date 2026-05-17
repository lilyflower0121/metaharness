#!/usr/bin/env python3
"""Infer commit/branch impact for agent-authored Git changes.

This helper is intentionally conservative. It does not prove safety; it routes
changes to the right review/audit weight and emits a compact decision card.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]

HIGH_PATTERNS = [
    ("auth_or_permission_surface", re.compile(r"(^|/)(auth|authz|permission|policy|session|identity|iam|rbac|acl)(/|\.|-|_)", re.I)),
    ("secret_or_credential_surface", re.compile(r"(^|/)(\.env|secret|credential|token|keychain|private[_-]?key|oauth|jwt)(/|\.|-|_|$)", re.I)),
    ("billing_or_account_surface", re.compile(r"(^|/)(billing|payment|invoice|subscription|account|finance)(/|\.|-|_)", re.I)),
    ("crypto_surface", re.compile(r"(^|/)(crypto|cryptography|encrypt|decrypt|signing|hashing)(/|\.|-|_)", re.I)),
    ("data_deletion_or_migration_surface", re.compile(r"(^|/)(migration|migrations|schema|delete|destructive|drop)(/|\.|-|_)", re.I)),
    ("ci_cd_or_deploy_surface", re.compile(r"(^|/)(\.github/workflows|deploy|release|terraform|infra|k8s|helm|dockerfile|Dockerfile)(/|\.|-|_|$)", re.I)),
]

MEDIUM_PATTERNS = [
    ("dependency_or_lockfile_changed", re.compile(r"(^|/)(package-lock\.json|pnpm-lock\.yaml|yarn\.lock|poetry\.lock|uv\.lock|requirements.*\.txt|pyproject\.toml|package\.json|Cargo\.toml|Cargo\.lock|go\.mod|go\.sum)(/|$)", re.I)),
    ("config_changed", re.compile(r"(^|/)(config|configs|settings|\.config)(/|\.|-|_|$)", re.I)),
    ("public_api_surface", re.compile(r"(^|/)(api|routes|controllers|handlers|server|client)(/|\.|-|_)", re.I)),
    ("generated_or_codegen_surface", re.compile(r"(^|/)(generated|codegen|templates?)(/|\.|-|_)", re.I)),
    ("harness_gate_or_policy_changed", re.compile(r"(^|/)(scripts|contracts|rules|skills|adapters|\.claude|AGENTS\.md|CLAUDE\.md)(/|$)", re.I)),
]

TEST_PATH = re.compile(r"(^|/)(tests?|spec|__tests__)(/|$)|(_test|\.test|\.spec)\.", re.I)
TEST_WEAKENING_ADDED = re.compile(r"^\+.*\b(skip|xfail|todo|mock|stub|assert\s+True|expect\(.+\)\.toBeTruthy\(\))\b", re.I)
TEST_ASSERTION_REMOVED = re.compile(r"^-.*\b(assert|expect\(|should\(|must\()", re.I)

@dataclass
class Change:
    status: str
    path: str
    old_path: str | None = None

@dataclass
class Audit:
    changes: list[Change]
    escalators: set[str] = field(default_factory=set)
    rationale: list[str] = field(default_factory=list)
    risky_files: list[str] = field(default_factory=list)
    tests_changed: bool = False
    test_weakening: bool = False

    @property
    def inferred_risk(self) -> str:
        high = {
            "auth_or_permission_surface",
            "secret_or_credential_surface",
            "billing_or_account_surface",
            "crypto_surface",
            "data_deletion_or_migration_surface",
            "ci_cd_or_deploy_surface",
            "test_weakening_detected",
        }
        if self.escalators & high:
            return "high"
        if self.escalators:
            return "medium"
        return "low"


def git(args: list[str], *, check: bool = True) -> str:
    proc = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True)
    if check and proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip())
    return proc.stdout


def parse_name_status(text: str) -> list[Change]:
    changes: list[Change] = []
    for raw in text.splitlines():
        if not raw.strip():
            continue
        parts = raw.split("\t")
        status = parts[0]
        if status.startswith("R") or status.startswith("C"):
            if len(parts) >= 3:
                changes.append(Change(status=status, old_path=parts[1], path=parts[2]))
        elif len(parts) >= 2:
            changes.append(Change(status=status, path=parts[1]))
    return changes


def changed_files(base: str, head: str) -> list[Change]:
    out = git(["diff", "--name-status", f"{base}..{head}"])
    return parse_name_status(out)


def diff_text(base: str, head: str) -> str:
    return git(["diff", "--unified=0", f"{base}..{head}"], check=False)


def add_pattern_escalators(audit: Audit) -> None:
    for ch in audit.changes:
        path = ch.path
        if TEST_PATH.search(path):
            audit.tests_changed = True
            audit.escalators.add("tests_changed")
        for label, pattern in HIGH_PATTERNS:
            if pattern.search(path):
                audit.escalators.add(label)
                audit.rationale.append(f"{label}: {path}")
                audit.risky_files.append(path)
        for label, pattern in MEDIUM_PATTERNS:
            if pattern.search(path):
                audit.escalators.add(label)
                audit.rationale.append(f"{label}: {path}")
                audit.risky_files.append(path)


def add_diff_escalators(audit: Audit, diff: str) -> None:
    current_file = ""
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            current_file = line.removeprefix("+++ b/")
            continue
        if line.startswith("--- a/"):
            continue
        if not TEST_PATH.search(current_file):
            continue
        if TEST_WEAKENING_ADDED.search(line) or TEST_ASSERTION_REMOVED.search(line):
            audit.test_weakening = True
            audit.escalators.add("test_weakening_detected")
            audit.rationale.append(f"test weakening signal in diff: {current_file}")
            return


def required_validators(audit: Audit) -> list[str]:
    validators = ["git_diff_check", "path_boundary_check", "commit_receipt"]
    if audit.tests_changed or audit.test_weakening:
        validators.append("test_weakening_review")
    if audit.inferred_risk in {"medium", "high"}:
        validators.extend(["focused_tests", "independent_codegate"])
    if audit.inferred_risk == "high":
        validators.extend(["human_approval", "rollback_plan", "security_review"])
    if "dependency_or_lockfile_changed" in audit.escalators:
        validators.append("dependency_audit")
    if "harness_gate_or_policy_changed" in audit.escalators:
        validators.append("independent_gate_policy_review")
    return list(dict.fromkeys(validators))


def audit_range(base: str, head: str) -> Audit:
    audit = Audit(changes=changed_files(base, head))
    add_pattern_escalators(audit)
    add_diff_escalators(audit, diff_text(base, head))
    return audit


def build_receipt(base: str, head: str, declared_risk: str | None) -> dict:
    audit = audit_range(base, head)
    files = [ch.path for ch in audit.changes]
    commit_sha = git(["rev-parse", head]).strip()
    parent_sha = git(["rev-parse", f"{head}^"], check=False).strip()
    tree_sha = git(["rev-parse", f"{head}^{{tree}}"]).strip()
    subject = git(["log", "-1", "--pretty=%s", head]).strip()
    author = git(["log", "-1", "--pretty=%an <%ae>", head]).strip()
    timestamp = git(["log", "-1", "--pretty=%cI", head]).strip()
    risk = audit.inferred_risk
    status = "needs_human" if risk == "high" else "unknown"
    return {
        "schema": "metaharness.commit_receipt.v0",
        "range": {"base": base, "head": head},
        "commit": {
            "sha": commit_sha,
            "parent_sha": parent_sha,
            "tree_sha": tree_sha,
            "message": subject,
            "author": author,
            "timestamp": timestamp,
        },
        "intent": {
            "objective": subject or "unknown",
            "non_goals": [],
            "allowed_paths": [],
        },
        "scope": {
            "changed_files": files,
            "public_surface_changed": "public_api_surface" in audit.escalators,
            "dependency_or_lockfile_changed": "dependency_or_lockfile_changed" in audit.escalators,
            "tests_changed": audit.tests_changed,
            "config_or_ci_changed": bool({"config_changed", "ci_cd_or_deploy_surface"} & audit.escalators),
            "external_side_effect_surface": bool({"billing_or_account_surface", "ci_cd_or_deploy_surface", "data_deletion_or_migration_surface"} & audit.escalators),
            "gate_or_policy_changed": "harness_gate_or_policy_changed" in audit.escalators,
        },
        "risk": {
            "declared": declared_risk or "unknown",
            "inferred": risk,
            "escalators": sorted(audit.escalators),
            "rationale": audit.rationale,
        },
        "validators": {
            "required": required_validators(audit),
            "run": [],
            "skipped_with_reason": [],
        },
        "results": {
            "status": status,
            "evidence_paths": [],
            "command_summaries": [],
            "residual_risks": [
                "This helper infers audit scope only; it does not prove semantic correctness.",
                "Branch/PR aggregate gates are still required before merge.",
            ],
            "rollback": f"git revert {commit_sha}" if commit_sha else "unknown",
        },
        "decision_card": {
            "commit": commit_sha,
            "risk": risk,
            "blast_radius": files,
            "claim": subject or "unknown",
            "evidence": [],
            "risky_lines": [],
            "failed_or_unknown_gates": required_validators(audit),
            "residual_risk": ["unrun validators", "cross-commit interactions"],
            "if_approved": "continue to branch/PR aggregate gate",
            "if_rejected": f"revert or fix commit {commit_sha}",
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Infer commit-scoped audit risk and emit a decision card.")
    ap.add_argument("--base", default="HEAD^", help="Base ref for git diff, default HEAD^")
    ap.add_argument("--head", default="HEAD", help="Head ref for git diff, default HEAD")
    ap.add_argument("--declared-risk", choices=["low", "medium", "high"], default=None)
    ap.add_argument("--json", action="store_true", help="Emit JSON receipt")
    ap.add_argument("--fail-on-high", action="store_true", help="Exit 1 when inferred risk is high")
    args = ap.parse_args()

    try:
        receipt = build_receipt(args.base, args.head, args.declared_risk)
    except Exception as exc:
        print(f"COMMIT AUDIT FAIL: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(receipt, indent=2))
    else:
        risk = receipt["risk"]["inferred"]
        print(f"COMMIT AUDIT: {args.base}..{args.head} inferred risk={risk}")
        for esc in receipt["risk"]["escalators"]:
            print(f"- escalator: {esc}")
        print("required validators:")
        for validator in receipt["validators"]["required"]:
            print(f"- {validator}")
        print("changed files:")
        for path in receipt["scope"]["changed_files"]:
            print(f"- {path}")

    if args.fail_on_high and receipt["risk"]["inferred"] == "high":
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
