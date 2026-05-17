# Commit-scoped Agent Delegation

Commit-scoped delegation uses small Git commits as **audit checkpoints** for coding agents. It is designed to reduce human review load without pretending that a small diff is automatically safe.

## Core principle

```text
one logical agent change
  -> one Git commit
  -> inferred impact/risk
  -> targeted validators
  -> commit receipt / decision card
  -> branch/PR aggregate gate
```

Small commits are not assurance. They are stable anchors for receipts, rollback, focused tests, and review routing.

## When to use

Use this pattern for agent-authored repository changes when:

- the task can be decomposed into logical changes;
- changed paths can drive useful test/audit selection;
- an independent tester or gate can review the builder's commit;
- the branch will still pass a final aggregate gate before merge/release.

Do not use commit-scoped audit as the only gate for auth, billing, cryptography, migrations, deletion, CI/CD, dependency, credential, or deployment changes.

## Roles

```text
planner/spec
  freezes the task contract, allowed paths, non-goals, and success criteria

codebuilder
  makes one logical change and one commit

codetester
  independently selects/runs focused checks and looks for verifier weakening

codegate
  validates the diff, receipt, inferred risk, rollback, and branch implications

human reviewer
  handles high-risk, failed, unknown, or policy-escalated decision cards
```

The codebuilder must not be the final validator for its own commit.

## Commit receipt fields

A useful commit receipt should include at least:

```yaml
schema: metaharness.commit_receipt.v0
commit:
  sha: <git sha>
  parent_sha: <parent sha>
  tree_sha: <tree sha>
  message: <subject>
  author: <agent or person>
  timestamp: <iso8601>
intent:
  requirement_id: <id>
  objective: <single logical change>
  non_goals: []
  allowed_paths: []
scope:
  changed_files: []
  public_surface_changed: false
  dependency_or_lockfile_changed: false
  tests_changed: false
  config_or_ci_changed: false
  external_side_effect_surface: false
risk:
  declared: low|medium|high
  inferred: low|medium|high
  escalators: []
validators:
  required: []
  run: []
  skipped_with_reason: []
results:
  status: pass|fail|blocked|needs_human
  evidence_paths: []
  command_summaries: []
  residual_risks: []
  rollback: <command or plan>
```

## Risk inference

Risk must be inferred by the harness/CI, not trusted from the agent. Escalate when any of these appear in the diff:

- authentication, authorization, permissions, identity, sessions, tokens;
- billing, payments, financial/account-affecting logic;
- cryptography, secrets, credential handling, `.env`-like paths;
- deletion, data export, migration, schema changes;
- CI/CD, deployment, Docker, Terraform, infrastructure, release scripts;
- dependency manifests, lockfiles, package manager config;
- test deletion, assertion removal, `skip`, `xfail`, broad mocks, snapshot mass updates;
- gate, policy, validator, or harness configuration changes;
- generated code or codegen templates that affect downstream artifacts.

## Gate stack

### Per-commit gate

- path boundary check;
- `git diff --check`;
- secret scan if available;
- focused tests based on changed paths;
- test-weakening detector;
- dependency/config/harness escalator detection;
- receipt generation.

### Branch/PR aggregate gate

Per-commit gates miss cross-commit interactions. Before merge:

- recompute cumulative branch risk;
- validate every receipt against commit/tree/parent hashes;
- rerun on the latest main/base after rebase;
- inspect the final whole-PR diff;
- run integration/E2E/security checks as risk requires;
- require human/CODEOWNER approval for high-risk surfaces.

## Anti-patterns

| ID | Anti-pattern | Why it fails | Required countermeasure |
| --- | --- | --- | --- |
| CAD-AP-001 | Small-commit safety illusion | A tiny diff can change auth, billing, data deletion, or deployment behavior. | Treat small commits as checkpoints only; infer risk from surfaces and branch context. |
| CAD-AP-002 | Risk laundering by split commits | A dangerous change can be split into many low-risk-looking commits. | Add branch cumulative risk and final whole-diff review. |
| CAD-AP-003 | Agent self-certification | The builder can rationalize its own diff and weak tests. | Separate codebuilder, codetester, and codegate. |
| CAD-AP-004 | Test weakening in the same commit | Passing tests can be caused by deleted assertions, skips, broad mocks, or snapshot churn. | Detect verifier weakening and require independent review. |
| CAD-AP-005 | Path-only impact analysis | Dynamic imports, config, feature flags, CI, and external APIs can bypass static file matching. | Add semantic/risk escalators and PR-level integration gates. |
| CAD-AP-006 | Receipt over-trust | A receipt proves selected checks ran, not that the change is safe. | Record skipped checks, residual risk, validator versions, and unknowns. |
| CAD-AP-007 | Receipt/hash drift | Rebase, squash, force-push, or amended commits can detach receipts from the reviewed tree. | Bind receipts to commit, tree, and parent hashes; revalidate after history rewrite. |
| CAD-AP-008 | Gate-policy tampering | An agent may change scripts, manifests, or policies that classify its own work. | Treat gate/policy changes as high-risk and validate them independently. |
| CAD-AP-009 | Commit spam review fatigue | Many small commits can overwhelm reviewers. | Collapse low-risk pass commits into decision cards and expand only exceptions. |
| CAD-AP-010 | Parallel context divergence | Subagents may implement inconsistent assumptions across branches or commits. | Share the frozen task contract, full relevant traces, and merge coordination state. |

## Decision card

Human review should see compressed exception-focused cards:

```yaml
decision_card:
  commit: <sha>
  risk: <inferred risk>
  blast_radius: <files/surfaces/users>
  claim: <what changed>
  evidence: <tests/scans/receipts>
  risky_lines: []
  failed_or_unknown_gates: []
  residual_risk: []
  rollback: <command or plan>
  if_approved: <effect>
  if_rejected: <rollback or fix path>
```

Low-risk passing commits can be collapsed. High-risk, failed, unknown, test-weakening, dependency, CI/CD, or policy/gate changes should expand automatically.

## Minimal local command

Use the portable audit helper to infer changed-file risk and emit a decision card:

```bash
python3 scripts/commit_scope_audit.py --base main --head HEAD --json
```

The helper is intentionally conservative. It is a routing gate, not a full security scanner.
