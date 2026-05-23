# Metaharness Architecture

Metaharness defines a harness rule architecture for autonomous AI-agent task execution.

The goal is to minimize user review while ensuring that the agent deterministically honors the user's purpose, constraints, non-goals, and safety boundaries.

## Design target

An agent run should be treated as bounded execution inside a harness:

```text
request → contract → evidence → plan → execution → validation → receipt → retention decision
```

The harness should prevent common autonomous-agent failures:

- objective drift
- silent scope expansion
- prohibited substitutions
- ungrounded assumptions
- unsafe external side effects
- scoped validation mistaken for global approval
- executor self-certification
- memory / rule bloat
- unverifiable success claims

## Layer 1: Intent Contract Layer

Freeze the user's intent before substantive execution.

Required fields:

- objective
- target user or job
- non-goals
- prohibited substitutions
- success criteria
- stop criteria
- authority source
- ambiguity owner
- scope-change rule
- scope boundary: in scope / out of scope / cannot harness / escalation triggers

The key invariant is that implementation convenience must not silently change the task. A second invariant is that a pass inside the contract must not be presented as approval outside the contract.

## Layer 2: Constraint & Policy Layer

Make constraints first-class inputs, not optional notes.

Typical constraints:

- allowed tools
- allowed paths, repositories, services, and models
- external-send policy
- destructive-action policy
- data classification
- secrets and PII handling
- public-repository safety
- cost, latency, and cloud-usage budgets

This layer should define both what is allowed and what is explicitly prohibited.

## Layer 3: Evidence & Context Layer

Control what the agent may rely on when making decisions.

Evidence classes:

- direct evidence: explicit user instruction, repository file, test result, command output
- contextual evidence: approved memory, skill, previous receipt, local project documentation
- weak evidence: model inference, stale memory, web summary, similar prior task
- prohibited evidence: unverified assumption, private data not authorized for the task, hidden context that cannot be cited

Evidence priority should be explicit so confidence does not outrank verification.

## Layer 4: Execution Decomposition Layer

Split non-trivial work into independently checkable roles.

Recommended separation:

- intake / router
- planner
- executor
- tester / evaluator
- final validator
- curator for retained lessons

For non-trivial work, the executor should not be the final certifier of its own output.

For code-development or artifact-construction work, the shared `artifact-build-flow-harness` layer owns the common flow: artifact design packet, build plan, bounded execution, validator suite, receipt, and retention. Risk-tier skills then add low/medium/high strictness.

For lifecycle control, `phase-risk-gate-harness` chooses different gates for exploration, MVP exploration, specification, implementation, merge, release, operate, and retention. This keeps early discovery fast while making merge/release/operation gates stricter.

Below every phase/risk gate, `lower-bound-gate-harness` enforces non-negotiable design and validation controls: objective integrity, authority boundaries, data/secret boundaries, untrusted input handling, allowed surfaces, evidence, stop/rollback, independent validation threshold, supply-chain boundary, and retention classification. This lower bound is placed in the contract so violations are caught before implementation, not only at final review.

For human review and publication, `io_publication` contracts plus `scripts/render_io.py` create static IO bundles from passed gate receipts. The IO layer publishes what was checked and why a gate passed, while access remains repository-permission inherited: same-repository Pages, repository-attached artifacts, or internal docs with mirrored repository ACLs. Task contracts should not choose arbitrary public/private visibility.

For runtime portability, `portable-agent-adapter-harness` keeps Claude Code, Codex, Hermes Agent, and other agents on the same shared command surface. Runtime files such as `CLAUDE.md`, `AGENTS.md`, and Hermes `SKILL.md` are adapters; they must point back to the shared contract and scripts rather than becoming separate policy sources.

For adoption into other repositories, this repository is the reference source, not the artifact to copy wholesale. Target repositories should classify each candidate artifact as `copy_as_is`, `copy_then_configure`, `adapt_policy`, `interpret_pattern`, `reference_only`, or `skip`. Standalone validators and schemas are often copyable; policy docs, examples, adapters, roles, and failure taxonomies usually need interpretation into the target repo's existing commands, CI, risk model, and policy source. See `docs/repository-adoption.md`.

## Layer 5: Validator Compilation Layer

Convert accepted requirements into checks whenever possible.

Examples:

- "do not break existing behavior" → regression tests
- "safe for public repo" → secret scan and public-release checklist
- "respect non-goals" → objective / non-goal diff check
- "this pass only covers X" → scope-boundary gate with out-of-scope, cannot-harness, accident scenarios, and escalation triggers
- "external side effects are controlled" → authority and rollback checklist
- "review burden is low" → compact receipt with evidence links

Natural-language rules should be compiled into executable tests, static checks, policy gates, or manual review checklists.

Metaharness starts with a lower-bound (LB) gate plus risk-tiered skills and structural gates:

```bash
python3 scripts/lb_gate.py --contract <contract.yaml>
python3 scripts/metaharness_gate.py --risk <low|medium|high> --contract <contract.yaml>
```

A task should not pass a gate merely because the agent read or summarized the rule; the relevant skill should name the validator that must pass for that risk tier.

Accepted feedback should also be compiled into a structured capture packet before it becomes durable policy. `contracts/activity-feedback-capture.schema.yaml` defines the portable packet shape for activity events, feedback events, requirement deltas, promotion decisions, and retention status. This keeps raw traces and user reactions as evidence, not as automatic requirements or authorization.

## Layer 6: Receipt & Audit Layer

A run is not complete until it leaves a reviewable receipt.

A minimal receipt records:

- objective
- scope
- files changed
- commands run
- tests or checks run
- validation status
- residual risks
- rollback path
- retention decision

The receipt should say why the run is considered valid, not merely that it succeeded.

## Layer 7: Retention Layer

Classify lessons before storing them.

Retention targets:

- stable user or workspace fact → memory / fact store
- reusable procedure → skill or reference
- failure pattern → eval case or guardrail
- repository-specific convention → repo documentation
- one-off detail → task receipt only
- obsolete or noisy context → discard

This prevents the harness from becoming unstable through accumulated contradictions and outdated rules.
