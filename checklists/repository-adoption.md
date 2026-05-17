# Repository Adoption Checklist

Use this when taking metaharness ideas into another repository. The goal is to make agents distinguish efficient copying from repo-specific interpretation.

## 1. Target repo discovery

- [ ] Existing `AGENTS.md`, `CLAUDE.md`, `.agent/`, README, CI, and release/security docs were read before adoption.
- [ ] Existing repo policy that is stronger than metaharness defaults is preserved.
- [ ] Target repo risk tier and lifecycle phase are identified.
- [ ] Local owner or maintainer for adopted harness files is identified.

## 2. Artifact classification

For each considered metaharness artifact, record one class:

- [ ] `copy_as_is` — deterministic and portable.
- [ ] `copy_then_configure` — portable shape, but target-specific values required.
- [ ] `adapt_policy` — principle must become local docs/tests/review gates.
- [ ] `interpret_pattern` — guidance only; summarize or reference.
- [ ] `reference_only` — useful background; do not import.
- [ ] `skip` — not relevant or too heavy.

## 3. Copy-safe checks

Before copying a file:

- [ ] No secrets, credentials, private paths, PII, or internal-only examples.
- [ ] No hidden dependency on a specific developer, runtime, or local machine state.
- [ ] Command can run from the target repo root.
- [ ] Required support files are also listed.
- [ ] License/provenance and upstream source version are recorded.
- [ ] Rollback is possible by reverting the adoption commit.

## 4. Interpretation checks

Before converting a principle into local policy:

- [ ] Target repo's existing workflow is not overwritten blindly.
- [ ] Local roles, phases, branches, CI jobs, and release gates are mapped explicitly.
- [ ] Non-applicable metaharness controls are documented as skipped, not silently dropped.
- [ ] Examples are rewritten with target repo paths, authority, validators, and rollback.
- [ ] Agent instruction files stay thin pointers to one local source of truth.

## 5. Validation

- [ ] Copied validators pass on at least one target-repo fixture or contract.
- [ ] Negative fixtures are included for any bypass the adoption is meant to prevent.
- [ ] Existing target repo tests/checks affected by the adoption pass.
- [ ] A receipt lists copied artifacts, interpreted controls, skipped artifacts, and residual risks.

## 6. Final receipt fields

The final adoption receipt should include:

- [ ] source metaharness commit or tag;
- [ ] copied files and whether they were configured;
- [ ] interpreted policies and target files changed;
- [ ] skipped artifacts and reasons;
- [ ] validators/checks run;
- [ ] rollback path;
- [ ] update policy for tracking future metaharness changes.
