---
name: minimum-floor-gate-harness
description: Use when enforcing non-negotiable lower-bound controls that apply below every risk/phase gate, including design-stage controls before implementation and validation-stage receipt checks before completion.
---

# Minimum Floor Gate Harness

## Purpose

Define the context-independent lower bound that every gated autonomous-agent task must satisfy before any risk- or phase-specific gate can pass.

Risk/phase gates decide how much extra work is needed. The minimum floor decides what is never acceptable.

## When to use

Use for any metaharness contract, especially when:

- creating a design contract before implementation;
- checking whether a task may proceed from exploration to implementation;
- reviewing a gate that seems too light for security/compliance/data/supply-chain concerns;
- adding a new agent runtime adapter;
- reducing user review without hiding unacceptable ambiguity.

## Required floor

Every gated contract must cover both design-stage and validation-stage controls.

### Design-stage controls

- objective integrity
- authority boundary
- data/secret boundary
- untrusted input boundary
- allowed surface
- evidence floor
- stop or rollback condition
- validator boundary
- supply-chain boundary or explicit not-applicable reason
- retention boundary

### Validation-stage controls

- evidence receipt
- side-effect read-back or explicit not-applicable reason
- secret/private-data check or explicit not-applicable reason
- changed-surface check
- validator result
- rollback/irreversibility result
- retention result

## Command

```bash
python3 scripts/minimum_floor_gate.py --contract <contract.yaml>
```

The portable suite runs it first:

```bash
python3 scripts/run_metaharness.py --contract <contract.yaml>
```

## Non-negotiable blockers

Do not proceed if:

- external/destructive/account-affecting side effects lack authority;
- data classification or external-send policy is missing;
- secrets/private data may leave allowed boundaries;
- untrusted content can become instruction without classification;
- changed paths/tools/services are unbounded;
- the task cannot name evidence stronger than model assertion;
- rollback/irreversibility and stop conditions are absent;
- non-trivial medium/high work relies on executor self-certification;
- dependency/build/release work has no provenance/supply-chain boundary;
- retention target is unspecified or would store secrets/session noise.

## Fixtures

- Valid: `contracts/examples/minimum-floor.medium.valid.yaml`
- Invalid: `contracts/examples/minimum-floor.invalid.yaml`

## References

- `docs/minimum-floor-gates.md`
- `references/minimum-floor-source-map.md`
