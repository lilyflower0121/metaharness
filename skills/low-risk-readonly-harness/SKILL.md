---
name: low-risk-readonly-harness
description: Use when an agent task is read-only, local, reversible, and has no external side effects. Requires evidence grounding and a lightweight receipt before completion.
version: 0.1.0
author: Metaharness Contributors
license: MIT
metadata:
  metaharness:
    risk_tier: low
    gate: scripts/metaharness_gate.py --risk low --contract <contract.yaml>
    tags: [risk-low, readonly, evidence, receipt]
---

# Low-Risk Read-Only Harness

## Overview

Use this skill for tasks where the agent reads, summarizes, inspects, drafts, or performs reversible local reasoning without changing durable state or contacting external parties.

Low risk does **not** mean unchecked. The gate is intentionally lightweight: objective, evidence, and receipt must exist, but side-effect authorization is not required when the task truly has no side effects.

## When to Use

Use when all are true:

- Work is read-only or draft-only.
- No files, repos, accounts, settings, cron jobs, credentials, or external messages are changed.
- No private data is sent to unapproved external services.
- Failure would be easy to correct and would not affect third parties.

Do not use when:

- The task writes files, commits, pushes, publishes, schedules automation, changes config, or sends messages.
- The task involves secrets, credentials, customer data, billing, security posture, or unattended execution.

## Required Contract Fields

A low-risk contract must include:

- `risk_tier: low`
- `objective`
- `non_goals`
- `constraints.external_side_effect_policy: none`
- `evidence_policy.required_sources`
- `validation.success_criteria`
- `stop_conditions`

## Code-Level Gate

This skill also ships a wrapper script and reference:

- `scripts/check_contract.py --contract <contract.yaml>` runs the low-risk gate.
- `references/read-only-evidence-receipt.md` describes the evidence receipt.

Run before marking the task complete:

```bash
python3 scripts/metaharness_gate.py --risk low --contract path/to/contract.yaml
```

The gate fails if required fields are missing, if external side effects are declared, or if validation evidence is absent.

## Completion Receipt

The final receipt must include:

- objective
- evidence used
- checks performed
- residual uncertainties
- retention decision

## Common Pitfalls

1. Treating low risk as no validation.
2. Letting stale memory override current files or instructions.
3. Reporting completion without direct evidence.
4. Accidentally crossing into medium risk by editing files or committing changes.

## Verification Checklist

- [ ] Contract declares `risk_tier: low`.
- [ ] No external or durable side effects are present.
- [ ] Evidence sources are listed.
- [ ] Validation success criteria are listed.
- [ ] `metaharness_gate.py --risk low` passes.
