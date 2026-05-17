---
name: artifact-build-flow-harness
description: Use when an agent must plan and execute a code-development or artifact-construction flow to achieve an objective. Provides the shared layer for contract, build, validation, receipt, and retention across risk tiers.
version: 0.1.0
author: Metaharness Contributors
license: MIT
metadata:
  metaharness:
    risk_tier: shared
    gate: scripts/artifact_flow_gate.py --contract <contract.yaml>
    tags: [artifact-flow, code-development, build, validation, receipt]
---

# Artifact Build Flow Harness

## Overview

This is the shared layer for tasks where the agent must construct something to achieve a purpose: code, documentation packages, schemas, generated assets, release artifacts, research packages, or task-specific deliverables.

Risk-specific skills decide how strict the gate is. This skill manages the common build-flow shape so every artifact-producing task has the same control points.

## When to Use

Use when the task involves:

- code development
- documentation or rule-set construction
- generated artifacts
- repository package creation
- repeatable scripts or pipelines
- any task where a build plan becomes a deliverable

Pair with one of:

- `low-risk-readonly-harness` for read-only planning or analysis
- `medium-risk-change-harness` for bounded local/repo changes
- `high-risk-side-effect-harness` for publication, credentials, deletion, cron, or account-impacting actions

## Shared Flow

1. Contract: freeze objective, non-goals, constraints, success criteria, and risk tier.
2. Design packet: describe artifact type, target users, interfaces, dependencies, and prohibited substitutions.
3. Build plan: map requirements to files, commands, and validators.
4. Execution: perform only allowed actions.
5. Validation: run risk-tier gate plus artifact-specific checks.
6. Receipt: record changed surfaces, evidence, validation result, residual risk, and rollback.
7. Retention: classify reusable lessons as memory, skill, eval, reference, repo doc, or discard.

## Required Contract Fields

In addition to the risk-tier contract, artifact-building tasks should include:

```yaml
artifact_flow:
  artifact_type: docs|code|schema|skill|script|release|other
  target_users:
    - ...
  deliverables:
    - ...
  build_steps:
    - ...
  validators:
    - ...
  acceptance_receipt: path-or-format
```

## Executable Gate

Run this shared gate before claiming artifact-flow readiness:

```bash
python3 scripts/artifact_flow_gate.py --contract path/to/contract.yaml
```

For full validation, also run the risk-tier gate:

```bash
python3 scripts/metaharness_gate.py --risk <low|medium|high> --contract path/to/contract.yaml
```

## References and Scripts

- `references/shared-artifact-build-flow.md` explains the common flow architecture.
- `scripts/make_artifact_contract.py` creates a starter contract.

## Common Pitfalls

1. Treating the build plan as the artifact instead of validating the produced artifact.
2. Losing non-goals during implementation.
3. Building without a receipt format.
4. Running only the shared flow gate and forgetting the risk-tier gate.

## Verification Checklist

- [ ] `artifact_flow` is present in the contract.
- [ ] Deliverables are named.
- [ ] Build steps are named.
- [ ] Validators are named.
- [ ] Acceptance receipt path or format is named.
- [ ] Shared artifact-flow gate passes.
- [ ] Risk-tier gate also passes.
