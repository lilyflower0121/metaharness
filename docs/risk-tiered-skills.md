# Risk-Tiered Skills

Metaharness rules should not remain prose-only. Each rule family should be packaged as a skill with a risk tier and an executable gate where possible.

## Risk tiers

| Tier | Typical work | Gate strength |
| --- | --- | --- |
| Low | Read-only inspection, summaries, local drafts | Objective, evidence, no side effects, receipt |
| Medium | File edits, commits, local config, docs/rules/schema changes | Bounded paths/tools, validation checks, rollback |
| High | Publishing, deletion, credentials, permissions, recurring jobs, billing/account effects | Explicit authority, target, rollback/irreversibility, independent validation, read-back verification |

## Skills

- [`skills/lower-bound-gate-harness`](../skills/lower-bound-gate-harness/SKILL.md) — non-negotiable lower bound for every gated task, enforced during design and validation
- [`skills/artifact-build-flow-harness`](../skills/artifact-build-flow-harness/SKILL.md) — shared layer for code-development and artifact-construction flows
- [`skills/phase-risk-gate-harness`](../skills/phase-risk-gate-harness/SKILL.md) — selects different checks by lifecycle phase and risk
- [`skills/portable-agent-adapter-harness`](../skills/portable-agent-adapter-harness/SKILL.md) — exposes the same gates to Claude Code, Codex, Hermes Agent, and other runtimes
- [`skills/low-risk-readonly-harness`](../skills/low-risk-readonly-harness/SKILL.md)
- [`skills/medium-risk-change-harness`](../skills/medium-risk-change-harness/SKILL.md)
- [`skills/high-risk-side-effect-harness`](../skills/high-risk-side-effect-harness/SKILL.md)
- [`skills/validator-gate-authoring`](../skills/validator-gate-authoring/SKILL.md)

Each skill should carry support files:

- `references/` for durable patterns and review criteria
- `scripts/` for executable gates, wrappers, fixture checks, or generators

## Gate command

```bash
python3 scripts/metaharness_gate.py --risk <low|medium|high> --contract <contract.yaml>
```

The gate validates structural obligations for the declared risk tier. It intentionally fails closed when risk-appropriate fields are missing.

## Current rule classification

| Rule | Risk tier | Skill |
| --- | --- | --- |
| Lower-bound (LB) | All | lower-bound-gate-harness |
| Intent freeze | Low+ | low-risk-readonly-harness, medium-risk-change-harness, high-risk-side-effect-harness |
| Evidence priority | Low+ | low-risk-readonly-harness |
| Executor / validator separation | Medium+ | medium-risk-change-harness, high-risk-side-effect-harness |
| Side-effect authorization | High | high-risk-side-effect-harness |
| Validator compilation | Meta | validator-gate-authoring |
| Code/artifact construction flow | Shared | artifact-build-flow-harness |
| Lifecycle phase selection | Shared | phase-risk-gate-harness |
| Runtime portability | Shared | portable-agent-adapter-harness |

## Design note

The first gate checks contract structure rather than full semantic truth. Task-specific validators should be added as separate scripts or schema refinements and referenced from `validation.automated_checks`.
