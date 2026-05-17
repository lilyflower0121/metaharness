---
name: phase-risk-gate-harness
description: Use when selecting gates for an agent task by both risk tier and process phase, so MVP exploration, specification, implementation, merge, release, operation, and retention get different checks.
version: 0.1.0
author: Metaharness Contributors
license: MIT
metadata:
  metaharness:
    risk_tier: shared
    gate: scripts/phase_risk_gate.py --contract <contract.yaml>
    tags: [phase-gates, risk-based, mvp, merge, release, operations]
---

# Phase Risk Gate Harness

## Overview

Use this skill to avoid both under-gating and over-gating. A read-only exploration task should not pay the cost of a release gate, while a release or unattended-operation task must not pass with MVP-level checks.

This skill composes with risk-tier skills and `artifact-build-flow-harness`.

## When to Use

Use for any objective-driven flow that has a lifecycle phase:

- exploration
- mvp_exploration
- specification
- implementation
- merge
- release
- operate
- retention

## Required Contract Fields

Every phase-gated contract needs:

```yaml
phase: implementation
risk_tier: medium
phase_controls:
  assumptions: []
  feedback_items: []
  requirement_validator_map: []
  changed_surfaces: []
  independent_validation: []
  release_targets: []
  operation_stop_rules: []
  retention_decisions: []
```

Only the fields relevant to the phase must be non-empty. The executable gate determines which ones are required.

## Executable Gate

```bash
python3 scripts/phase_risk_gate.py --contract path/to/contract.yaml
```

For artifact-producing work, also run:

```bash
python3 scripts/artifact_flow_gate.py --contract path/to/contract.yaml
python3 scripts/metaharness_gate.py --risk <risk> --contract path/to/contract.yaml
```

## Phase Rules

- Exploration: require evidence and assumptions; block irreversible side effects.
- MVP exploration: require learning goal, feedback classification, and non-goals; block production/release substitution.
- Specification: require requirement-to-validator mapping.
- Implementation: require changed surfaces, validators, and rollback.
- Merge: require independent validation and receipt.
- Release: require authority, target, rollback/irreversibility, and read-back plan.
- Operate: require stop rules, monitoring/log evidence, and owner.
- Retention: require classification of memory, skill, eval, reference, repo doc, or discard.

## References and Scripts

- `references/phase-risk-gate-matrix.md` gives the full matrix.
- `scripts/check_phase_contract.py` runs the root phase-risk gate.

## Common Pitfalls

1. Applying release-grade gates to early exploration and slowing learning.
2. Allowing MVP exploration to create durable external side effects.
3. Merging without independent validation because implementation checks passed.
4. Operating unattended automation without stop rules.
5. Storing every lesson in always-loaded memory.

## Verification Checklist

- [ ] Contract has `phase` and `risk_tier`.
- [ ] Phase-specific fields are present.
- [ ] Risk-tier gate also passes when applicable.
- [ ] Artifact-flow gate passes for artifact-producing tasks.
- [ ] Gate strength matches phase rather than defaulting to maximum weight.
