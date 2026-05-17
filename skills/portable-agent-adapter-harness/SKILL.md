---
name: portable-agent-adapter-harness
description: Use when making metaharness reusable across Claude Code, Codex, Hermes Agent, or another coding-agent runtime while preserving a single executable gate contract.
---

# Portable Agent Adapter Harness

## Purpose

Expose metaharness to multiple agent runtimes without duplicating policy logic in each agent's prompt files.

The invariant is:

> Agent-specific files are adapters. The shared contract, scripts, fixtures, and receipts are the harness.

## When to use

Use this skill when:

- adding Claude Code, Codex, Hermes Agent, OpenCode, or another coding-agent integration;
- creating `CLAUDE.md`, `AGENTS.md`, `.claude/commands`, Hermes skills, or other runtime instructions;
- deciding how a gated task should be completed by different agents;
- preventing adapter drift between agent runtimes.

## Workflow

1. Identify the runtime: `claude`, `codex`, `hermes`, or `generic`.
2. Keep policy in shared files:
   - `scripts/run_metaharness.py`
   - `scripts/metaharness_gate.py`
   - `scripts/phase_risk_gate.py`
   - `scripts/artifact_flow_gate.py`
   - `contracts/`
   - `skills/`
3. Install or merge the thin adapter:
   - Claude Code: `adapters/claude/CLAUDE.md`
   - Codex: `adapters/codex/AGENTS.md`
   - Hermes Agent: `adapters/hermes/SKILL.md`
4. Require the universal command before completion:

```bash
python3 scripts/run_metaharness.py --contract <contract.yaml>
```

5. Require a receipt in the final answer:
   - contract path
   - risk tier
   - phase
   - validators run
   - pass/fail
   - residual risks

## Gate

Validate adapter package integrity with:

```bash
python3 scripts/check_agent_adapters.py
```

Run a contract through the universal gate with:

```bash
python3 scripts/run_metaharness.py --contract contracts/examples/merge.medium.valid.yaml
```

## Pitfalls

- Do not paste the full metaharness policy into `CLAUDE.md` or `AGENTS.md`; it will drift.
- Do not make Claude-specific slash commands the source of truth.
- Do not let Codex/Hermes use a different risk definition than Claude.
- Do not treat an agent's narrative summary as a gate receipt.
- Do not mark completion without executing the shared runner or explicitly reporting why no gate applies.

## Supporting files

- `references/adapter-contract.md`
- `scripts/emit_adapter.py`
