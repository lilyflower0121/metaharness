# Agent Runtime Adapters

This directory contains thin adapters for using metaharness from different autonomous coding-agent runtimes.

Adapters are not the source of truth. Shared scripts and contracts are.

- `claude/CLAUDE.md` — Claude Code project memory adapter.
- `claude/commands/metaharness-gate.md` — optional Claude Code slash command.
- `codex/AGENTS.md` — Codex repo instruction adapter.
- `hermes/SKILL.md` — Hermes Agent skill adapter.

Validate adapters with:

```bash
python3 scripts/check_agent_adapters.py
```
