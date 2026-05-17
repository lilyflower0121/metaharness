# Metaharness Agent Instructions

This file is the generic entrypoint for any agent runtime that reads `AGENTS.md` or repo-root instructions. It is an adapter, not the policy source of truth.

## First read

1. Read `.agent/RESOLVER.md` to resolve the task type, required contract, and validation route.
2. Use shared repo files as the source of truth:
   - `README.md` — repo purpose and map.
   - `docs/repository-adoption.md` — how target repos decide what to copy, configure, adapt, interpret, reference, or skip.
   - `checklists/repository-adoption.md` — review checklist for adopting metaharness into another repo.
   - `docs/architecture.md` — seven-layer harness model.
   - `docs/failure-mode-catalog.md` — gateable anti-patterns and failures.
   - `docs/phase-risk-gates.md` — lifecycle phase gates.
   - `docs/lower-bound-gates.md` — non-negotiable lower-bound controls.
   - `docs/commit-scoped-agent-delegation.md` — coding-agent Git checkpoint pattern.
   - `contracts/` — schemas and examples.
   - `scripts/` — executable validators and helpers.
   - `skills/` — reusable harness skills and references.
3. Do not copy or reinterpret policy into this file. If policy changes, update shared docs/scripts/contracts and then update adapters only as pointers.

## Adoption into target repositories

When using metaharness in another repository, do not assume the target should copy this whole repo. First read the target repo's own instructions, then classify each candidate artifact as `copy_as_is`, `copy_then_configure`, `adapt_policy`, `interpret_pattern`, `reference_only`, or `skip` using `docs/repository-adoption.md`. Deterministic validators and schemas are the most copyable; docs, examples, adapters, role names, authority rules, and release policy usually need target-specific interpretation.

## Contract requirement

Create or update a contract under `contracts/` when the task includes any of:

- code, script, schema, adapter, rule, checklist, or documentation changes that affect harness behavior;
- multi-file edits;
- git commit, merge, release, publish, or IO publication;
- configuration, credentials, security, compliance, cron, or automation;
- external side effects or irreversible/destructive actions;
- retained learning in skills, evals, references, or memory-like docs.

Small read-only exploration may proceed without a contract, but the final answer must say why no gate applied and cite the evidence read.

## Universal validation commands

Before claiming completion for a gated task, run the shared suite:

```bash
python3 scripts/run_metaharness.py --contract <contract.yaml>
```

For adapter/instruction changes, also run:

```bash
python3 scripts/check_agent_adapters.py
```

For agent-authored Git changes, generate or inspect a commit/branch decision card:

```bash
python3 scripts/commit_scope_audit.py --base <base> --head <head> --json
```

## Delegation failure-mode guard

Before delegating to a subagent or another runtime, include a compact delegation packet with objective, non-goals, allowed surfaces, required sources/files, expected output schema, verification commands/read-backs, risk tier, and handoff-back requirements. A subagent summary is not completion until the parent verifies the referenced evidence.

## Coding-agent delegation rule

For non-trivial repository changes, use independent roles conceptually even if one runtime executes them sequentially:

```text
planner/spec -> codebuilder -> codetester -> codegate -> human exception review
```

- One logical change per commit when committing.
- The builder cannot be the final validator for its own change.
- Test deletion, assertion weakening, `skip`/`xfail`, broad mocks, snapshot churn, and gate-policy changes are review blockers or escalation triggers.
- Branch/PR aggregate gates are required because per-commit checks miss cross-commit interactions.

## Final response receipt

Report:

- contract path or no-contract reason;
- risk tier and lifecycle phase;
- validators/checks run and pass/fail;
- changed files or commit SHAs;
- evidence/read-back paths;
- residual risks and rollback path.
