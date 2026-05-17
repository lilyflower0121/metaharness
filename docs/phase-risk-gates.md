# Phase and Risk Based Gates

Metaharness gates are two-dimensional:

1. **Risk tier**: low, medium, high.
2. **Process phase**: exploration, specification, implementation, merge, release, operate, retention.

This avoids slowing every task with the heaviest gate while still blocking high-impact failures.

## Phase definitions

| Phase | Purpose | Gate emphasis |
| --- | --- | --- |
| `exploration` | Learn, inspect, prototype, compare options | Evidence, assumptions, no irreversible side effects |
| `mvp_exploration` | Build/use a small MVP to elicit feedback | Feedback classification, non-goals, no premature hardening |
| `specification` | Freeze what will be built | Objective, constraints, requirement-to-validator mapping |
| `implementation` | Build within the contract | Allowed surfaces, tests/checks, rollback |
| `merge` | Accept into main/shared state | Independent validation, receipt, clean status, public safety |
| `release` | Publish or expose externally | Authority, provenance, rollback, read-back |
| `operate` | Run unattended or recurring behavior | Stop rules, monitoring, audit, alerting |
| `retention` | Store reusable learning | classify memory/skill/eval/reference/discard |

## Gate matrix

| Phase | Low risk | Medium risk | High risk |
| --- | --- | --- | --- |
| exploration | evidence + assumptions | evidence + explicit non-goals | evidence + untrusted-source/data boundaries |
| mvp_exploration | learning goals | feedback ledger + non-goals | redaction + no external side effect |
| specification | objective + stop conditions | validator map + allowed surfaces | authority precheck + data classification |
| implementation | local checks | tests + rollback + allowed paths | authority + sandbox + rollback |
| merge | receipt | independent validator + clean diff | public safety + provenance + approval |
| release | read-back | read-back + rollback | explicit approval + durable read-back + audit |
| operate | status check | stop rules + logs | monitoring + kill switch + audit |
| retention | discard/session note | skill/eval candidate | human-reviewed retention only |

## Minimality rule

A gate should be just strong enough for the risk and phase, but it may never bypass the lower-bound (LB) in `docs/lower-bound-gates.md`.

- Do not require merge-grade checks during early MVP exploration.
- Do not let MVP exploration perform release-grade side effects.
- Do not let implementation proceed with a vague spec if the next phase is merge or release.
- Do not skip read-back verification after publication because tests passed locally.
- Do not accept any phase/risk shortcut that omits authority, data boundary, allowed surface, evidence, stop/rollback, validator, supply-chain, or retention lower-bound controls.

## Executable gate

```bash
python3 scripts/lb_gate.py --contract <contract.yaml>
python3 scripts/phase_risk_gate.py --contract <contract.yaml>
```

The script validates `risk_tier`, `phase`, and phase-specific required fields. Use it together with:

```bash
python3 scripts/metaharness_gate.py --risk <risk> --contract <contract.yaml>
python3 scripts/artifact_flow_gate.py --contract <contract.yaml>
```
