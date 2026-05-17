# Portable Agent Adapters

Metaharness must be reusable across Claude Code, Codex, Hermes Agent, and other coding agents without depending on a single vendor runtime.

The portable contract is:

1. Keep the source-of-truth rules in normal repo files: `contracts/`, `docs/`, `skills/`, and `scripts/`.
2. Give each agent a thin adapter that points to the same scripts and contract fields.
3. Do not duplicate policy logic inside each agent prompt. Prompts route to executable gates.
4. Treat agent-specific files as adapters, not as the harness itself.

## Adapter targets

### Claude Code

Use `adapters/claude/CLAUDE.md` as the project memory file, or include its content from an existing `CLAUDE.md`.

Recommended placement:

```text
CLAUDE.md
.claude/commands/metaharness-gate.md
```

Claude Code should run:

```bash
python3 scripts/run_metaharness.py --contract <contract.yaml>
```

before claiming a gated task is complete.

### Codex

Use `adapters/codex/AGENTS.md` as the repo instruction file, or merge it into an existing `AGENTS.md`.

Codex should run the same command:

```bash
python3 scripts/run_metaharness.py --contract <contract.yaml>
```

Use `codex exec` prompts that reference contract path, risk tier, phase, allowed surfaces, and required validators.

### Hermes Agent

Use `adapters/hermes/SKILL.md` as a Hermes-compatible skill. It routes Hermes tasks to the same contract and script interface.

Recommended installation:

```bash
mkdir -p ~/.hermes/skills/metaharness-portable-agent-adapter
cp adapters/hermes/SKILL.md ~/.hermes/skills/metaharness-portable-agent-adapter/SKILL.md
```

Hermes should use the same validator runner and report the receipt path.

## Universal command surface

The common entrypoint is:

```bash
python3 scripts/run_metaharness.py --contract <contract.yaml>
```

It composes:

- `metaharness_gate.py`
- `phase_risk_gate.py`
- `artifact_flow_gate.py` when `artifact_flow` is present

Future validators should be added through a manifest rather than per-agent prose.

## Why adapters stay thin

Agent-specific instruction files are always at risk of drifting apart. Keep them thin:

- explain when to invoke metaharness;
- require the shared command;
- require receipts/evidence;
- do not restate the entire policy.

If a rule changes, update `scripts/`, `contracts/`, or `skills/`, then regenerate or update the adapters.
