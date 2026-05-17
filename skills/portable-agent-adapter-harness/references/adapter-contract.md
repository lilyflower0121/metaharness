# Adapter Contract

A metaharness-compatible agent adapter must satisfy these requirements.

## Required behavior

1. It must point to the shared gate runner:

```bash
python3 scripts/run_metaharness.py --contract <contract.yaml>
```

2. It must require the agent to keep task state in a contract file or explicitly say why the task is below gate threshold.
3. It must require evidence/read-back before claiming external side effects succeeded.
4. It must not redefine risk tiers inconsistently with `scripts/metaharness_gate.py`.
5. It must not redefine lifecycle phases inconsistently with `scripts/phase_risk_gate.py`.
6. It must require final output to include a receipt or the receipt path.

## Adapter-specific mapping

- Claude Code: `CLAUDE.md` + optional `.claude/commands/metaharness-gate.md`.
- Codex: `AGENTS.md` repository instructions.
- Hermes Agent: `SKILL.md` with references/scripts.

## Drift rule

If adapters disagree, shared scripts win. Update adapters to point back to the shared scripts.
