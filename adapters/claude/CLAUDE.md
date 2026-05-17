# Metaharness Adapter for Claude Code

This repository uses metaharness for risk- and phase-based autonomous-agent gates.

## Core rule

Start from repo-root `AGENTS.md`, then read `.agent/RESOLVER.md` to resolve task mode, risk, phase, contract need, and validator route.

Do not treat this file as the policy source of truth. The shared harness lives in:

- `contracts/`
- `skills/`
- `docs/`
- `scripts/`

Before claiming completion for a gated task, run:

```bash
python3 scripts/run_metaharness.py --contract <contract.yaml>
```

## When a contract is required

Create or update a contract when the task includes:

- code development or artifact construction;
- multi-file changes;
- git commit, merge, release, publish, or external side effects;
- credential/config/security/compliance-sensitive work;
- unattended or recurring operation;
- retained learning, skill, memory, or eval changes.

Small read-only answers may cite why no gate applies.

## Required final receipt

Final response must include:

- contract path or reason no contract was required;
- risk tier;
- lifecycle phase;
- validators run;
- result;
- residual risk.

## Phase/risk reminder

Exploration/MVP gates are lighter. Merge/release/operate gates are heavier. High-risk side effects require authority, rollback or irreversibility note, and read-back verification.
