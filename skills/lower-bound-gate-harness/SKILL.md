---
name: lower-bound-gate-harness
description: Use when enforcing non-negotiable lower-bound (LB) controls that apply below every risk/phase gate, including design-stage controls before implementation and validation-stage controls before completion.
---

# Lower-Bound (LB) Gate Harness

## Purpose

The lower-bound (LB) gate defines the non-negotiable minimum below every metaharness gate. Risk and phase gates can become lighter or heavier, but they cannot go below the LB.

## When to use

Use this skill for every contract that will be checked by metaharness, especially when:

- a task is being classified as low risk or early-phase;
- a task has external side effects, secrets, private data, dependencies, build/release surfaces, or retention decisions;
- an agent runtime adapter needs a shared safety floor across Claude Code, Codex, Hermes Agent, or another executor.

## Required LB

Every gated contract should include `lower_bound.design_controls` and `lower_bound.validation_controls`.

Design controls:

- objective integrity
- authority boundary
- data boundary
- untrusted-input boundary
- allowed surface
- evidence lower bound
- stop/rollback or irreversibility boundary
- validator boundary
- supply-chain boundary
- retention boundary

Validation controls:

- evidence receipt
- side-effect read-back or not-applicable reason
- secret/private-data check
- changed-surface check
- validator result
- rollback/irreversibility result
- retention result

## Procedure

1. Add the LB section before implementation, not after.
2. If an item is not applicable, write `not_applicable: <reason>` rather than `N/A` or `none`.
3. Run:

```bash
python3 scripts/lb_gate.py --contract <contract.yaml>
```

4. For the full suite, run:

```bash
python3 scripts/run_metaharness.py --contract <contract.yaml>
```

5. If LB fails, do not bypass it by picking a lighter phase/risk gate. Either fill the missing design control, move back to exploration, or ask for authority/scope clarification.

## Compatibility

Older contracts may contain `minimum_floor`; `scripts/lb_gate.py` accepts it as a legacy alias. New public contracts should use `lower_bound`, and public docs should use **LB** / **lower-bound** terminology.

## Pitfalls

- Treating low risk as no authority/data/evidence/rollback requirements.
- Adding LB only to receipts; it must exist in the design contract before execution.
- Allowing vague values such as `TBD`, `none`, or `N/A`.
- Treating a successful local command as proof of external side effects.
- Retaining secrets, private data, or session noise as memory/skills.

## Verification

- `scripts/lb_gate.py` passes on valid fixtures.
- invalid LB fixture fails.
- `scripts/run_metaharness.py` runs LB before risk/phase/artifact gates.
