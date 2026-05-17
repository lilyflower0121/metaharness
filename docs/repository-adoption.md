# Repository Adoption Guide

Metaharness is a shared reference harness. A target repository should not copy the whole repository or treat every file here as mandatory runtime policy. Agents adopting metaharness into another repository must first classify each artifact as copy, adapt, interpret, reference, or skip.

## Adoption rule

Use the narrowest artifact that gives the target repository an enforceable improvement.

```text
metaharness reference -> adoption classification -> repo-specific contract -> minimal copied files -> validators -> receipt
```

The adoption output should be a small, repo-local harness layer, not a full clone of this repository inside the target repo.

## Artifact classes

| Class | Meaning | Typical action |
| --- | --- | --- |
| `copy_as_is` | Portable executable or schema can be used without semantic changes. | Copy with provenance and run the same check in the target repo. |
| `copy_then_configure` | The artifact is portable, but paths, phases, risk tiers, or command names must be filled in. | Copy a template or script, then edit target-specific configuration. |
| `adapt_policy` | The rule expresses a reusable control, but the target repo must decide how to enforce it. | Translate into local `AGENTS.md`, docs, tests, CI, or review checklists. |
| `interpret_pattern` | The artifact is explanatory guidance or a failure-mode taxonomy. | Extract relevant principles; do not paste wholesale as binding policy. |
| `reference_only` | Useful background that should stay in metaharness or a linked source. | Cite it in a receipt or design note; do not import. |
| `skip` | Not relevant, too heavy, or unsafe for this repo. | Record no-adoption reason if it was considered. |

Use `adapt_policy` when the target repo will enforce a rule locally. Use `interpret_pattern` when the target repo only extracts rationale, vocabulary, workflow shape, or failure-mode awareness.

## Default classification by path

| Metaharness path | Default adoption class | Notes for target repos |
| --- | --- | --- |
| `scripts/*_gate.py`, `scripts/run_metaharness.py` | `copy_as_is` or `copy_then_configure` | Copy only the validators the target repo will actually invoke. Keep commands stable and add target-specific wrappers only when needed. |
| `contracts/*.schema.yaml` | `copy_as_is` or `copy_then_configure` | Schemas are intended to be portable, but examples and required fields may need target repo vocabulary. |
| `contracts/examples/*.valid.yaml` | `copy_then_configure` | Examples are fixtures, not policy. Replace objective, paths, authority, validators, rollback, and evidence sources. |
| `AGENTS.md`, `.agent/RESOLVER.md`, `adapters/*` | `adapt_policy` | Use as a thin-adapter pattern. Do not overwrite an existing repo's agent instructions without preserving local conventions. |
| `skills/*/SKILL.md` | `adapt_policy` | Import as repo-local skills only when the trigger, workflow, and validator command are relevant. |
| `skills/*/references/*` | `interpret_pattern` or `reference_only` | Usually background rationale. Link or summarize the part that matters. |
| `docs/*.md` | `interpret_pattern` | Docs explain controls. Convert only relevant controls into local gates/checklists. |
| `checklists/*.md` | `copy_then_configure` or `adapt_policy` | Keep items that match the repo's risk model; remove non-applicable items explicitly. |
| `patterns/*.md` | `interpret_pattern` or `adapt_policy` | Use as workflow templates; bind to local commands and roles. |
| `rules/*.md` | `adapt_policy` | Rules become useful only when target repo validators or review gates enforce them. |
| `evals/*` | `copy_then_configure` | Import recurring failure cases that the target repo can reproduce. |
| `io/*` | `copy_then_configure` | Only when the target repo needs same-repository review surfaces. Preserve repository-inherited visibility. |

## What can be copied efficiently

Copying is efficient when all of these are true:

1. The artifact has no private paths, secrets, repo-specific owners, or runtime-only assumptions.
2. Its inputs and outputs are already file-based and deterministic.
3. The target repo can run the same command without depending on hidden local services.
4. The artifact is small enough to maintain in the target repo.
5. The receiving repo has a clear owner for keeping it updated.

Good copy candidates:

- standalone validators with local file inputs;
- schema files and fixture shapes;
- compact checklists after target-specific trimming;
- thin adapter stubs that point to a local resolver;
- negative fixtures for known bypasses.

## What must be interpreted before adoption

Interpret before importing when the artifact contains:

- risk or lifecycle policy that may conflict with the target repo's release process;
- human-role assumptions such as `codebuilder`, `codetester`, `codegate`, or reviewer ownership;
- path allowlists, data classifications, or authority rules;
- examples that mention metaharness-specific files;
- public-repo safety constraints that differ for private/internal repos;
- operational rules for recurring jobs, publication, or external side effects.

For these, the agent should write a target-specific adoption note or contract that says which control is being adopted, how it is enforced locally, and what was intentionally left out.

## Non-goals

Do not:

- vendor the full metaharness repository into every project;
- paste metaharness docs into a target repo as unowned policy;
- make target repo `AGENTS.md` a duplicate policy source;
- treat examples as production contracts;
- adopt high-risk gates for low-risk exploration without a reason;
- weaken a target repo's stronger existing policy because metaharness has a smaller default;
- copy public examples that contain target-private details.

## Minimal target-repo adoption packet

When an agent incorporates metaharness into another repository, it should leave a compact packet in the target repo or final receipt:

```yaml
metaharness_adoption:
  source_version: <commit-or-tag>
  target_repo: <repo-name>
  adoption_goal: <why this repo needs the harness>
  adopted:
    - source: scripts/lb_gate.py
      class: copy_as_is
      target: scripts/lb_gate.py
      local_owner: <role-or-team>
      local_decision: copied unchanged because the target repo uses the same contract shape and command surface
      verification: python3 scripts/lb_gate.py --contract <contract.yaml>
    - source: docs/phase-risk-gates.md
      class: interpret_pattern
      target: docs/agent-harness.md
      local_decision: extracted phase names but mapped validators to existing CI jobs
  skipped:
    - source: io/
      reason: target repo does not publish review surfaces
  local_policy_sources:
    - AGENTS.md
    - docs/agent-harness.md
  validators:
    - python3 scripts/run_metaharness.py --contract <contract.yaml>
  update_policy: review metaharness upstream only when changing local agent harness policy
```

## Agent adoption workflow

1. Read the target repo's existing `AGENTS.md`, `README`, CI, scripts, and security/release docs first.
2. Classify desired metaharness artifacts with the adoption classes above.
3. Prefer copying only deterministic validators, schemas, fixtures, and thin pointers.
4. Translate policy docs into repo-local controls instead of pasting them wholesale.
5. Add or update a target-repo contract/receipt that records the adoption decision.
6. Run the smallest meaningful local validator and any target repo tests affected by the adoption.
7. Report copied files, interpreted controls, skipped artifacts, verification, and rollback.

## Verification questions

Run the adoption gate when a contract contains `metaharness_adoption`:

```bash
python3 scripts/adoption_gate.py --contract <repository-adoption-contract.yaml>
python3 scripts/run_metaharness.py --contract <repository-adoption-contract.yaml>
```

Positive and negative fixtures:

```bash
python3 scripts/adoption_gate.py --contract contracts/examples/repository-adoption.medium.valid.yaml
python3 scripts/adoption_gate.py --contract contracts/examples/repository-adoption.invalid.yaml  # expected FAIL
```

Before claiming adoption is complete, answer:

- Which artifacts were copied byte-for-byte or with configuration changes?
- Which principles were interpreted into local policy, and where?
- Which metaharness artifacts were intentionally not adopted?
- Does the target repo have a single source of truth for agent policy?
- Can the target repo run the copied validators without this repo checked out?
- Did the adoption preserve or strengthen the target repo's existing safety policy?
