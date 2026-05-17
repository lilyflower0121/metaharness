# Metaharness Resolver

This resolver tells any agent how to interpret this repository without depending on a vendor-specific memory file. Treat it as the routing index. Normative behavior still lives in `contracts/`, `scripts/`, `docs/`, and `skills/`.

## Resolution order

When starting a task in this repo, resolve in this order:

1. **Task mode** — read the user request and choose one mode from the table below.
2. **Risk tier** — infer `low`, `medium`, or `high`; do not trust only the agent's declaration.
3. **Lifecycle phase** — infer `exploration`, `mvp_exploration`, `specification`, `implementation`, `merge`, `release`, `operate`, or `retention`.
4. **Contract need** — decide whether a `contracts/*.yaml` task contract is required.
5. **Validator route** — run the smallest shared validator set that proves the intended behavior is reachable.
6. **Receipt** — report contract, validators, evidence, residual risk, and rollback.

## Task-mode router

| If the task is about... | Read first | Contract? | Required validators |
| --- | --- | --- | --- |
| Understanding the repo, read-only explanation | `README.md`, `docs/architecture.md`, relevant docs | Usually no | Cite files read; no-gate reason |
| Creating/changing harness docs, rules, checklists, skills, adapters, or scripts | `docs/architecture.md`, `docs/failure-mode-catalog.md`, relevant target file | Yes for non-trivial/multi-file | `run_metaharness.py`; focused script/doc check |
| Coding-agent delegation or Git checkpointing | `docs/commit-scoped-agent-delegation.md`, `patterns/coding-pipeline.md` | Yes | `commit_scope_audit.py`, `run_metaharness.py` |
| Lower-bound controls | `docs/lower-bound-gates.md`, `skills/lower-bound-gate-harness/SKILL.md` | Yes | `scripts/lb_gate.py` via `run_metaharness.py` |
| Phase/risk gates | `docs/phase-risk-gates.md`, `skills/phase-risk-gate-harness/SKILL.md` | Yes | `scripts/phase_risk_gate.py` via `run_metaharness.py` |
| Artifact construction flow | `skills/artifact-build-flow-harness/SKILL.md`, `skills/artifact-build-flow-harness/references/shared-artifact-build-flow.md` | Yes | `run_metaharness.py` plus artifact-flow gate when `artifact_flow` exists |
| Portable agent adapters / AGENTS / CLAUDE / Hermes skill | `docs/portable-agent-adapters.md`, `adapters/*`, this resolver | Yes | `scripts/check_agent_adapters.py`, `run_metaharness.py` |
| IO publication or review surfaces | `docs/io-publishing.md`, `io/README.md` | Yes | `run_metaharness.py`; renderer check when publishing |
| Retention, skillization, eval capture | `docs/failure-mode-catalog.md`, relevant `skills/` or `evals/` | Usually yes | retention decision in receipt; relevant gate suite |

## Risk-tier resolver

Infer the minimum risk from surfaces touched:

- **Low**: read-only explanation, examples, typo/docs change with no policy effect, reversible local-only edits.
- **Medium**: scripts, schemas, validators, adapters, skills, contracts, multi-file docs that affect behavior, repository instructions, generated artifacts.
- **High**: external side effects, publish/release/deploy, credentials/secrets, auth/permission, data deletion/export, migrations, CI/CD, dependency/supply-chain changes, gate-policy changes that could weaken enforcement.

If declared and inferred risk differ, use the higher tier or record the disagreement as an escalation.

## Lifecycle phase resolver

- `exploration`: read-only investigation, no changes.
- `mvp_exploration`: prototype or learning artifact, no irreversible side effects.
- `specification`: contract/schema/rule design before implementation.
- `implementation`: files are changed locally.
- `merge`: final branch/PR readiness, aggregate diff and receipt checks.
- `release`: publish, tag, package, external IO, or user-visible deployment.
- `operate`: recurring/unattended job, monitoring, or runtime behavior.
- `retention`: memory/skill/eval/reference capture or pruning.

## Mandatory lower-bound checks

Every gated task must preserve:

- objective integrity;
- authority for external/destructive/account-affecting side effects;
- data/secret boundary;
- untrusted-input boundary;
- allowed file/tool surface;
- evidence receipt over assertion;
- stop/rollback or irreversibility note;
- independent validation threshold;
- supply-chain boundary;
- retention classification.

See `docs/lower-bound-gates.md`.

## Validator command resolver

Use these commands from repo root:

```bash
# Full shared suite for a contract
python3 scripts/run_metaharness.py --contract <contract.yaml>

# Adapter integrity
python3 scripts/check_agent_adapters.py

# Commit/branch impact routing
python3 scripts/commit_scope_audit.py --base <base> --head <head> --json

# IO rendering, only when producing a review surface
python3 scripts/render_io.py --contract <contract.yaml> --receipt <receipt.json> --out <dir>
```

Do not replace these with narrative claims. If a command cannot be run, explain why and mark the result as unverified.

## File ownership map

| Path | Purpose | Notes |
| --- | --- | --- |
| `AGENTS.md` | Generic repo-root agent adapter | Thin pointer to this resolver and shared commands |
| `.agent/RESOLVER.md` | Cross-runtime routing index | Update when adding new task modes or validator routes |
| `adapters/` | Vendor/runtime-specific adapters | Must stay thin; validate with `check_agent_adapters.py` |
| `contracts/` | Schemas and example contracts | Keep examples public-safe and validator-compatible |
| `docs/` | Shared rationale and policy docs | Normative docs should point to executable validators |
| `patterns/` | Reusable execution patterns | Coding flow, delegation patterns |
| `rules/` | Small normative rules | Avoid duplicating full docs |
| `scripts/` | Executable gate runners/helpers | Policy enforcement belongs here or in contracts |
| `skills/` | Reusable skill packages | Use references/scripts; avoid always-loaded bloat |
| `io/` | Human-reviewable IO publication support | Access must be repository-inherited |
| `evals/` | Regression/failure cases | Add recurring failures here |
| `checklists/` | Human/manual review aids | Should complement, not replace, validators |

## Adapter invariant

`AGENTS.md`, `CLAUDE.md`, Hermes `SKILL.md`, slash commands, and future adapters must not become divergent policy sources. They should only:

1. identify that metaharness applies;
2. point to this resolver and shared docs;
3. require a contract or no-gate reason;
4. invoke shared validator commands;
5. require a receipt in the final answer.

## Stop conditions

Stop and ask for human direction or report blocked if:

- the task requires external/destructive/account-affecting action without explicit authority;
- no suitable contract exists and the task is medium/high risk;
- validator output fails and the failure is not intentionally being fixed;
- required evidence is unavailable;
- the requested change would make an adapter or prompt file the policy source of truth;
- a command would need secrets, private credentials, or network access not authorized by the contract.
