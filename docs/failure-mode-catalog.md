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

## Phase principle

The same risk does not require the same gate at every phase.

- MVP exploration optimizes learning speed and should block irreversible side effects, not demand production-grade completeness.
- Specification freezes intent and should block ambiguity, unclassified feedback, and requirement-to-validator gaps.
- Implementation allows bounded changes and should require allowed surfaces, build steps, tests, and rollback.
- Merge requires independent validation, clean status, receipt, and public/supply-chain checks when relevant.
- Release/operate requires authority, monitoring, rollback/stop rules, and read-back verification.

See `docs/phase-risk-gates.md` and `skills/phase-risk-gate-harness`.
