# metaharness

Metaharness is a public, implementation-neutral repository for codifying harness rules that let AI agents execute tasks autonomously while minimizing user review and deterministically honoring objectives and constraints.

It is based on operational lessons from Hermes Agent, but the artifacts here should stay portable: contracts, rules, schemas, checklists, patterns, examples, and eval cases that can be reused by other agent runtimes.

## Core purpose

Reduce repeated human steering by making the workflow itself enforce:

- frozen task intent
- explicit constraints and non-goals
- evidence-grounded decisions
- side-effect authorization
- executor / evaluator / validator separation
- validation receipts
- disciplined retention of reusable lessons

Metaharness is **not** a prompt dump. It is an architecture for binding agent execution to contracts, evidence, policy gates, validators, and audit receipts.

## Repository map

```text
metaharness/
  adapters/    Thin runtime adapters for Claude Code, Codex, Hermes Agent
  principles/   Human-readable design principles
  contracts/    Machine-readable schemas and task packets
  rules/        Normative harness rules
  patterns/     Reusable task pipeline patterns
  checklists/   Preflight, validation, security, release checks
  examples/     Concrete sample harness packets
  evals/        Failure cases and regression scenarios
  docs/         Glossary and design rationale
  scripts/      Executable validators and portable gate runners
  skills/       Harness skills with references and support scripts
```

## Initial architecture

The initial architecture is organized as seven layers:

1. Intent Contract Layer
2. Constraint & Policy Layer
3. Evidence & Context Layer
4. Execution Decomposition Layer
5. Validator Compilation Layer
6. Receipt & Audit Layer
7. Retention Layer

See [`docs/architecture.md`](docs/architecture.md).

## Risk-tiered skills and gates

Harness rules should be packaged as skills with risk-appropriate validators, not only prose to read and understand.

Initial skills:

- [`skills/minimum-floor-gate-harness`](skills/minimum-floor-gate-harness/SKILL.md) — non-negotiable lower-bound controls enforced at design and validation time
- [`skills/artifact-build-flow-harness`](skills/artifact-build-flow-harness/SKILL.md) — shared flow for code development and artifact construction
- [`skills/phase-risk-gate-harness`](skills/phase-risk-gate-harness/SKILL.md) — selects gates by lifecycle phase as well as risk tier
- [`skills/portable-agent-adapter-harness`](skills/portable-agent-adapter-harness/SKILL.md) — keeps Claude Code, Codex, Hermes Agent, and other runtimes on the same executable gate contract
- [`skills/low-risk-readonly-harness`](skills/low-risk-readonly-harness/SKILL.md)
- [`skills/medium-risk-change-harness`](skills/medium-risk-change-harness/SKILL.md)
- [`skills/high-risk-side-effect-harness`](skills/high-risk-side-effect-harness/SKILL.md)
- [`skills/validator-gate-authoring`](skills/validator-gate-authoring/SKILL.md)

Each skill has its own `references/` and `scripts/` support files. Common artifact-building flows are managed by `artifact-build-flow-harness`; risk-specific strictness is added by the low/medium/high skills.

Run the structural gates directly with:

```bash
python3 scripts/minimum_floor_gate.py --contract <contract.yaml>
python3 scripts/metaharness_gate.py --risk <low|medium|high> --contract <contract.yaml>
python3 scripts/phase_risk_gate.py --contract <contract.yaml>
```

For Claude Code, Codex, Hermes Agent, and other agent runtimes, prefer the portable suite entrypoint:

```bash
python3 scripts/run_metaharness.py --contract <contract.yaml>
```

See [`docs/minimum-floor-gates.md`](docs/minimum-floor-gates.md), [`docs/risk-tiered-skills.md`](docs/risk-tiered-skills.md), [`docs/phase-risk-gates.md`](docs/phase-risk-gates.md), and [`docs/portable-agent-adapters.md`](docs/portable-agent-adapters.md).

## Status

Early public scaffold. Interfaces and schema names may change until the first tagged release.
