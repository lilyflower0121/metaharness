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

The key invariant is that implementation convenience must not silently change the task.

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

## Layer 5: Validator Compilation Layer

Convert accepted requirements into checks whenever possible.

Examples:

- "do not break existing behavior" → regression tests
- "safe for public repo" → secret scan and public-release checklist
- "respect non-goals" → objective / non-goal diff check
- "external side effects are controlled" → authority and rollback checklist
- "review burden is low" → compact receipt with evidence links

Natural-language rules should be compiled into executable tests, static checks, policy gates, or manual review checklists.

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
