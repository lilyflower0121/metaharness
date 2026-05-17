---
name: metaharness-portable-agent-adapter
description: Use metaharness from Hermes Agent by routing tasks through shared contracts and executable gate scripts.
---

# Metaharness Portable Agent Adapter

## Purpose

Use the same metaharness contracts and validators that Claude Code and Codex use.

## Trigger

Use for tasks involving:

- code development or artifact construction;
- risk/phase gate validation;
- merge/release/publish/external side effects;
- skill/memory/eval/retention changes;
- autonomous or recurring operations.

## Workflow

1. Read repo-root `AGENTS.md`, then `.agent/RESOLVER.md` to resolve task mode, risk, phase, contract need, and validator route.
2. Determine whether a contract is required.
3. If required, create or update a contract under `contracts/`.
4. Run:

```bash
python3 scripts/run_metaharness.py --contract <contract.yaml>
```

5. Do not claim completion if the gate fails.
6. Final response includes contract path, risk tier, phase, validators, status, and residual risks.

## Authority

High-risk side effects require explicit authority, rollback or irreversibility handling, and read-back verification.
