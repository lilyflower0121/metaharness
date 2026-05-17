# Metaharness Adapter for Codex

This repository uses metaharness to gate autonomous coding-agent work.

## Source of truth

Start from repo-root `AGENTS.md`, then read `.agent/RESOLVER.md` to resolve task mode, risk, phase, contract need, and validator route.

Shared policy and validators live in:

- `contracts/`
- `skills/`
- `docs/`
- `scripts/`

Do not duplicate or reinterpret the policy in this file.

## Completion rule

For gated work, Codex must run:

```bash
python3 scripts/run_metaharness.py --contract <contract.yaml>
```

A task is not complete if this command fails.

## Contract triggers

Use a contract for:

- code development or artifact construction;
- medium/high risk file changes;
- merge/release/publish/external side effects;
- configuration, credentials, security, compliance, cron, or automation;
- retention into memory/skills/evals/references.

Read-only exploration may remain low risk but should still capture assumptions and evidence when non-trivial.

## Final answer

Report:

- contract path;
- risk tier;
- phase;
- validators run;
- pass/fail;
- evidence/read-back;
- residual risks.
