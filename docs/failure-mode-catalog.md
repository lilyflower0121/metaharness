# Failure Mode Catalog

This catalog turns repeated feedback and common external research findings into gateable failure modes.

## Source classes

Internal feedback distilled into this repo:

- Prose-only rules do not reliably block behavior.
- High-risk actions must not share the same weak gate as read-only work.
- Code-development and artifact-construction flows need a shared layer.
- Every important skill should carry executable scripts and references.
- Executor summaries are evidence, not validation.
- User review is scarce; gates should filter routine issues before asking.

External reference families used as pattern sources:

- OWASP Top 10 for LLM Applications: prompt injection, data leakage, insecure output handling, excessive agency, supply-chain and tool risks.
- NIST AI RMF: govern/map/measure/manage framing, documented risk treatment, context-specific controls.
- SLSA / supply-chain guidance: provenance, dependency integrity, build/release separation.
- OWASP ASVS-style verification: explicit controls and testable requirements rather than intent-only security claims.

## Lower-bound (LB)

Some failures sit below risk/phase selection and must be blocked in both design and validation stages. See `docs/lower-bound-gates.md` and `skills/lower-bound-gate-harness`.

Lower-bound (LB) families:

- LB-001 Objective integrity
- LB-002 Authority for side effects
- LB-003 Data and secret boundary
- LB-004 Untrusted input boundary
- LB-005 Allowed surface
- LB-006 Evidence over assertion
- LB-007 Stop/rollback
- LB-008 Independent validation threshold
- LB-009 Supply-chain baseline
- LB-010 Retention boundary

## Canonical failure modes

| ID | Failure mode | Typical phase | Risk | Gate family |
| --- | --- | --- | --- | --- |
| FM-001 | Objective drift | all | low+ | intent / phase gate |
| FM-002 | Prohibited substitution | exploration, implementation, merge | medium+ | contract and acceptance gate |
| FM-003 | Missing evidence / hallucinated success | all | low+ | evidence and receipt gate |
| FM-004 | Prose-only policy | specification, implementation, merge | medium+ | validator compilation gate |
| FM-005 | Executor self-certification | implementation, merge | medium+ | independent validation gate |
| FM-006 | Unbounded file/tool surface | implementation, merge | medium+ | allowed surface gate |
| FM-007 | Missing rollback or irreversibility note | implementation, merge, release | medium+ | rollback gate |
| FM-008 | Unauthorized external side effect | merge, release, operate | high | authority gate |
| FM-009 | Secret / private data leak | implementation, merge, release | high | public safety / data gate |
| FM-010 | Prompt/tool injection or untrusted instruction capture | exploration, implementation, operate | high | evidence provenance gate |
| FM-011 | Supply-chain or dependency drift | implementation, merge, release | high when public/prod | dependency/provenance gate |
| FM-012 | MVP anchoring as accepted requirement | mvp_exploration | medium | feedback classification gate |
| FM-013 | Premature production hardening during MVP | mvp_exploration | low/medium | phase-appropriate scope gate |
| FM-014 | Skipping tests/checks before merge | merge | medium+ | merge readiness gate |
| FM-015 | Unattended automation without stop rules | operate | high | operations gate |
| FM-016 | Retention bloat or stale always-loaded rules | operate, retention | medium | retention classification gate |
| FM-017 | Small-commit safety illusion | implementation, merge | medium+ | commit receipt + PR aggregate gate |
| FM-018 | Risk laundering by split commits | implementation, merge | high when sensitive | cumulative branch risk gate |
| FM-019 | Test weakening hidden in agent commit | implementation, merge | medium+ | test-weakening detector + independent tester |
| FM-020 | Receipt/hash drift after rebase or squash | merge | medium+ | commit/tree/parent receipt integrity gate |
| FM-021 | Gate-policy tampering by the builder | implementation, merge | high | independent gate-policy review |
| FM-022 | Framing omission before delegation | exploration, specification | medium+ | anti-rework front gate |
| FM-023 | Hidden preconditions skipped | exploration, implementation | medium+ | prerequisite discovery gate |
| FM-024 | Tool/path anchoring | exploration, implementation | low+ | alternative-lane gate |
| FM-025 | Context density failure | all | medium | context budget / evidence narrowing gate |
| FM-026 | File or artifact handoff unread | delegation, implementation, merge | medium+ | file-read receipt gate |
| FM-027 | Tool-surface / MCP schema tax | exploration, implementation, operate | medium+ | tool allowlist and lazy-schema gate |
| FM-028 | Delegation contract loss | delegation, implementation | medium+ | subtask contract and read-back gate |
| FM-029 | Parallel subagent state conflict | delegation, implementation, merge | medium+ | shared-state and integration gate |
| FM-030 | Multi-agent communication overhead | delegation, operate | medium | structured-state compression gate |
| FM-031 | Recursive delegation runaway | delegation, operate | high | spawn-depth / budget / no-recursive-scheduling gate |
| FM-032 | Test overtrust / agent-generated tests overfit | implementation, merge | medium+ | independent evaluator and hidden-assumption gate |
| FM-033 | Regression blindness in harness evolution | implementation, merge, release | medium+ | regression-risk manifest and rollback gate |
| FM-034 | Final-output-only review | all | medium+ | trajectory exception and tool/action audit gate |
| FM-035 | A2A scope creep / delegated authority expansion | delegation, operate | high | handoff allowlist and payload validation gate |
| FM-036 | Reliability metric flattening | evaluation, merge, operate | medium | multi-axis reliability evaluation gate |
| FM-037 | Human review bottleneck / review fatigue | merge, release, operate | medium+ | review compression and exception-routing gate |
| FM-038 | Final-format extraction failure | all | low+ | schema/output-shape validation and repair gate |
| FM-039 | Prompt-only accumulation | specification, operate, retention | medium | move-to-validator/skill/reference gate |

## Agent development / delegation anti-patterns

These modes come from `/Users/lily/cowork/research/paper/2026-05-17_agent_development_delegation_failure_modes.md` and should be converted into validators or receipts where possible.

- **Framing omission**: do not enter implementation/delegation without objective, non-goals, alternative frames, and a wrong-if condition.
- **Hidden preconditions**: record local availability, permissions, data/API/auth/source quality, and critical unknowns before execution.
- **Tool/path anchoring**: include primary/fallback/spike/reject lanes when a tool/model/path choice could change the result.
- **Context density failure**: use file map → search hit → narrow slice; do not pass full corpora or full tool schema when a compact evidence packet is enough.
- **File/artifact handoff unread**: a file path is not evidence until the receiver records a read-back path, line range, hash, or inspected handle.
- **Tool-surface/MCP tax**: expose only task-relevant tools and load full schemas lazily after intent/state/risk filtering.
- **Delegation contract loss**: every subagent packet needs objective, non-goals, allowed surfaces, required sources/files, output schema, verification, risk, and handoff-back fields.
- **Parallel subagent inconsistency**: parallelize exploration/review first; parallel implementation requires disjoint surfaces, shared state packets, and integration gates.
- **Multi-agent communication overhead**: pass structured state, claim/evidence maps, failure states, and receipts; keep raw trace for drill-down.
- **Recursive delegation runaway**: enforce max depth, budget, stop conditions, and no recursive scheduling unless explicitly authorized.
- **Test overtrust**: agent-generated tests are useful evidence but not final proof; combine them with existing tests, hidden assumptions, diff review, and independent evaluation.
- **Regression blindness**: every harness/skill/tool/memory/gate change should name expected fixes, at-risk regressions, verification, and rollback.
- **Final-output-only review**: inspect trajectory exceptions, tool calls, permissions, and side effects, not only the final artifact.
- **A2A scope creep**: structured handoff requests must validate target, payload, authority, data boundary, and tool inheritance.
- **Reliability metric flattening**: do not accept a single solve-rate/pass-rate; track consistency, robustness, predictability, safety, latency/cost, and human review load.
- **Human review bottleneck**: route humans to failed, unknown, high-risk, side-effect, and policy-exception cases; convert repeated review comments into validators.
- **Final-format extraction failure**: distinguish bad reasoning from malformed output; use schema validation and repair passes when the trace contains enough evidence.
- **Prompt-only accumulation**: do not keep appending prose instructions; move recurring failures into validators, scripts, skills, references, or eval cases.

## Commit-scoped delegation anti-patterns

Commit-scoped audit is a useful review-load reducer, but only if it is treated as a checkpoint layer inside a branch/PR assurance system.

- **Small commits are not safety guarantees.** A one-line change can affect auth, billing, deletion, migration, CI/CD, or deployment behavior.
- **Split commits can launder risk.** Recompute risk cumulatively at branch/PR level and inspect the final whole diff.
- **Passing tests can be verifier weakening.** Treat test deletion, assertion removal, `skip`/`xfail`, broad mocks, and snapshot churn as blockers or human-review triggers.
- **Receipts can drift.** Bind receipts to commit, tree, and parent hashes; revalidate after rebase, squash, amend, or force-push.
- **Gate changes are high risk.** Scripts, schemas, policies, skills, adapters, and rules that classify work must not be self-approved by the same builder.

See `docs/commit-scoped-agent-delegation.md`.

## Phase principle

The same risk does not require the same gate at every phase.

- MVP exploration optimizes learning speed and should block irreversible side effects, not demand production-grade completeness.
- Specification freezes intent and should block ambiguity, unclassified feedback, and requirement-to-validator gaps.
- Implementation allows bounded changes and should require allowed surfaces, build steps, tests, and rollback.
- Merge requires independent validation, clean status, receipt, and public/supply-chain checks when relevant.
- Release/operate requires authority, monitoring, rollback/stop rules, and read-back verification.

See `docs/phase-risk-gates.md` and `skills/phase-risk-gate-harness`.
