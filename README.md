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

## Adoption model

Metaharness is a shared reference harness, not a repository that every target project should vendor wholesale. Agents adopting it into another repository must classify each artifact before importing it:

- `copy_as_is` — deterministic validators, schemas, or fixtures that can run unchanged;
- `copy_then_configure` — portable templates that need target paths, commands, authority, or rollback filled in;
- `adapt_policy` — controls that must become target-repo instructions, tests, CI, or review gates;
- `interpret_pattern` — explanatory patterns or failure taxonomies to summarize, not paste as binding policy;
- `reference_only` / `skip` — background or non-applicable material.

Start with [`docs/repository-adoption.md`](docs/repository-adoption.md), [`checklists/repository-adoption.md`](checklists/repository-adoption.md), and [`contracts/metaharness-adoption.schema.yaml`](contracts/metaharness-adoption.schema.yaml). Target repos should keep a single local policy source and import only the smallest enforceable subset.

## Repository map

```text
metaharness/
  AGENTS.md    Generic repo-root instructions for any agent runtime
  .agent/      Cross-runtime resolver and routing index
  adapters/    Thin runtime adapters for Claude Code, Codex, Hermes Agent
  io/          Static IO publishing templates for human-reviewable gate receipts
  principles/   Human-readable design principles, including repo-driven design systems
  contracts/    Machine-readable schemas, task packets, and commit receipts
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

- [`skills/lower-bound-gate-harness`](skills/lower-bound-gate-harness/SKILL.md) — non-negotiable lower-bound controls enforced at design and validation time
- [`skills/artifact-build-flow-harness`](skills/artifact-build-flow-harness/SKILL.md) — shared flow for code development and artifact construction
- [`skills/phase-risk-gate-harness`](skills/phase-risk-gate-harness/SKILL.md) — selects gates by lifecycle phase as well as risk tier
- [`skills/portable-agent-adapter-harness`](skills/portable-agent-adapter-harness/SKILL.md) — keeps Claude Code, Codex, Hermes Agent, and other runtimes on the same executable gate contract
- [`skills/low-risk-readonly-harness`](skills/low-risk-readonly-harness/SKILL.md)
- [`skills/medium-risk-change-harness`](skills/medium-risk-change-harness/SKILL.md)
- [`skills/high-risk-side-effect-harness`](skills/high-risk-side-effect-harness/SKILL.md)
- [`skills/validator-gate-authoring`](skills/validator-gate-authoring/SKILL.md)

Activity and feedback capture:

- [`docs/activity-feedback-capture.md`](docs/activity-feedback-capture.md) — how to structure what the agent did, what feedback arrived, which deltas were accepted, and what was retained
- [`contracts/activity-feedback-capture.schema.yaml`](contracts/activity-feedback-capture.schema.yaml) — portable schema for JSONL/database/event-log implementations
- [`checklists/activity-feedback-capture.md`](checklists/activity-feedback-capture.md) — manual review checklist for privacy, feedback disposition, promotion, and retention

Scope and boundary control:

- [`docs/scope-boundary-harness.md`](docs/scope-boundary-harness.md) — require in-scope, out-of-scope, cannot-harness, accident-scenario, and escalation declarations so scoped validation is not mistaken for global approval

Repo-driven design systems:

- [`principles/repo-driven-design-systems.md`](principles/repo-driven-design-systems.md) — make production repositories the source of truth for UI tokens, components, pages, flows, and design review evidence
- [`docs/repo-driven-design-system-migration.md`](docs/repo-driven-design-system-migration.md) — migration pattern for retiring detached design-tool authority while keeping human-verifiable review surfaces
- [`checklists/repo-driven-design-system-migration.md`](checklists/repo-driven-design-system-migration.md) — manual gate for token-to-flow migration, new UI proposals, PR evidence, and retirement decisions

Research task metaharnesses:

- [`docs/research-task-metaharness.md`](docs/research-task-metaharness.md) — expected-value harness pattern for research outputs that feed downstream artifacts, decisions, workflows, or services
- [`docs/candidate-selection-research-pattern.md`](docs/candidate-selection-research-pattern.md) — subordinate pattern for candidate-producing research tasks: discovery, identity, evidence, confusable cases, and allowed-use scope

Each skill has its own `references/` and `scripts/` support files. Common artifact-building flows are managed by `artifact-build-flow-harness`; risk-specific strictness is added by the low/medium/high skills.

Run the structural gates directly with:

```bash
python3 scripts/lb_gate.py --contract <contract.yaml>
python3 scripts/metaharness_gate.py --risk <low|medium|high> --contract <contract.yaml>
python3 scripts/phase_risk_gate.py --contract <contract.yaml>
python3 scripts/adoption_gate.py --contract <repository-adoption-contract.yaml>
python3 scripts/scope_boundary_gate.py --contract <contract-with-scope-boundary.yaml>
python3 scripts/activity_feedback_gate.py --packet <activity-feedback-packet.yaml>
python3 scripts/commit_scope_audit.py --base main --head HEAD --json
```

For Claude Code, Codex, Hermes Agent, and other agent runtimes, start from `AGENTS.md` and `.agent/RESOLVER.md`, then prefer the portable suite entrypoint:

```bash
python3 scripts/run_metaharness.py --contract <contract.yaml>
```

See [`docs/lower-bound-gates.md`](docs/lower-bound-gates.md), [`docs/risk-tiered-skills.md`](docs/risk-tiered-skills.md), [`docs/phase-risk-gates.md`](docs/phase-risk-gates.md), [`docs/portable-agent-adapters.md`](docs/portable-agent-adapters.md), [`docs/commit-scoped-agent-delegation.md`](docs/commit-scoped-agent-delegation.md), and [`docs/io-publishing.md`](docs/io-publishing.md).

## Status

Early public scaffold. Interfaces and schema names may change until the first tagged release.
