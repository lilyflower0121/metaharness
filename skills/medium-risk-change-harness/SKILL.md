---
name: medium-risk-change-harness
description: Use when an agent task changes files, repository state, local configuration, generated artifacts, or workflow rules but remains reversible and does not perform high-risk external/account side effects.
version: 0.1.0
author: Metaharness Contributors
license: MIT
metadata:
  metaharness:
    risk_tier: medium
    gate: scripts/metaharness_gate.py --risk medium --contract <contract.yaml>
    tags: [risk-medium, file-changes, git, validation, rollback]
---

# Medium-Risk Change Harness

## Overview

Use this skill when the task modifies durable local or repository state but the change is bounded and reversible: documentation edits, code changes, local config edits, commits, generated artifacts, or workflow rule updates.

Medium-risk tasks must pass a stronger gate than read-only work: changed surfaces, rollback path, validation commands, and receipt evidence are mandatory.

## When to Use

Use when any are true:

- Files are created, modified, or deleted.
- A git commit or branch is created.
- Local configuration or scripts are changed.
- Documentation, skills, rules, schemas, or checklists are updated.
- Generated artifacts are added to a repository.

Escalate to high risk when:

- The task publishes, sends messages, alters credentials, changes access controls, schedules unattended jobs, or affects accounts/billing.
- The rollback path is unclear or the action is not safely reversible.

## Required Contract Fields

A medium-risk contract must include:

- `risk_tier: medium`
- `objective`
- `non_goals`
- `prohibited_substitutions`
- `constraints.allowed_paths`
- `constraints.allowed_tools`
- `constraints.external_side_effect_policy`
- `validation.automated_checks` or `validation.manual_checks`
- `validation.validator_role`
- `rollback.rollback_path`
- `stop_conditions`

## Code-Level Gate

This skill also ships a wrapper script and reference:

- `scripts/check_contract.py --contract <contract.yaml>` runs the medium-risk gate.
- `references/reversible-change-validation.md` describes bounded change validation.

Run before merging, pushing, or reporting completion:

```bash
python3 scripts/metaharness_gate.py --risk medium --contract path/to/contract.yaml
```

The gate fails if changed surfaces are not bounded, validation is missing, or rollback is undefined.

## Required Receipt Evidence

The validation receipt should include:

- files changed
- commands run
- tests/checks run
- validation status
- rollback path
- residual risks

## Common Pitfalls

1. Shipping markdown-only policy without executable checks.
2. Committing files outside the allowed path list.
3. Letting the implementer self-certify without a validation role.
4. Treating a successful commit or push as proof that the harness passed.

## Verification Checklist

- [ ] Contract declares `risk_tier: medium`.
- [ ] Allowed paths/tools are explicit.
- [ ] Validation commands or manual checks are explicit.
- [ ] Rollback path is present.
- [ ] `metaharness_gate.py --risk medium` passes.
