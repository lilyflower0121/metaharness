# Metaharness IO Publishing

Metaharness IO is a companion review surface for gate receipts and inspected evidence. It is derived from a metaharness-enabled repository and should contain **reviewable outputs**, not the entire working context.

## Purpose

Use IO when humans with repository access need to review what an agent did and why a harness gate passed:

- task objective, phase, and risk tier;
- LB / risk / phase / artifact gate results;
- commands that were run and their pass/fail status;
- evidence pointers and validation receipts;
- residual risk and retention notes;
- repository-bound access policy.

The IO surface is intentionally static. It can be hosted by same-repository Pages, a repository-attached artifact, or an internal docs target that mirrors repository permissions.

## Access model

Metaharness IO is **repository-permission inherited**. A task contract must not choose arbitrary `public`, `private`, or `internal` visibility. The view audience is the repository readers/reviewers for the source repository.

| Source/work repo | Allowed IO host | Who can view |
| --- | --- | --- |
| public repo | same-repo Pages or same-repo artifact | same as repository readers: everyone |
| private repo | same-repo private/internal Pages or repository-attached artifact | users with repository access |
| internal enterprise repo | same-repo/internal Pages or artifact | organization/internal readers |

Rule: **do not give agents freedom to select a wider or different publication target**. The renderer checks the contract declares `access_model: repository_inherited`; the actual access-control boundary remains the repository or artifact host.

## Contract section

A task that will publish IO should add:

```yaml
io_publication:
  access_model: repository_inherited
  audience:
    - repository_readers
    - maintainers
    - reviewers
  publish_target: same_repository_pages   # same_repository_pages | same_repository_artifact | repository_attached_artifact
  include:
    - gate_summary
    - validator_outputs
    - evidence_pointers
    - residual_risks
  redact:
    - secrets
    - private_data
    - absolute_local_paths
  human_review:
    required: true
    reviewer_role: repository_reader_or_maintainer
```

`visibility` is intentionally absent. Repository permissions define visibility. If a different audience is needed, create or choose a repository/artifact host with the desired permissions first, then publish IO there.

## Generation flow

1. Run the metaharness suite and save the JSON receipt:

```bash
python3 scripts/run_metaharness.py --contract <contract.yaml> --json > receipt.json
```

2. Render a static human-review bundle:

```bash
python3 scripts/render_io.py \
  --contract <contract.yaml> \
  --receipt receipt.json \
  --out site/io/<task-id>
```

3. Attach or publish the generated directory through a repository-synchronized target:

- same repository Pages;
- same repository CI artifact;
- internal docs target whose ACL mirrors the source repository.

## Required properties

An IO bundle must be:

- **reviewable**: a human can see which gates ran and which evidence was checked;
- **bounded**: it does not dump raw logs or secrets by default;
- **traceable**: links back to contract path, receipt schema, commit, and validator names;
- **repository-scoped**: access model is inherited from the source repository, not chosen per task;
- **static**: no remote JS, no external analytics, no hidden network calls.

## Non-goals

- IO is not a replacement for repository access control.
- IO is not a complete audit log for every token or tool call.
- IO does not prove semantic correctness; it publishes gate evidence for review.
- IO must not publish credentials, private chat logs, customer data, or full raw terminal dumps outside the repository-synchronized review boundary.
- IO must not be used as a general public marketing site unless the repository itself is public and the receipt is public-safe.

## Repository layout options

Recommended patterns:

```text
metaharness/                 # rules, contracts, gates
  scripts/render_io.py
  docs/io-publishing.md
  site/io/                   # generated pages, published only via repo-synced host
```

or inside a consuming repo:

```text
some-private-project/
  .metaharness/contracts/
  .metaharness/receipts/
  site/io/                   # generated, hosted with same repo permissions
```

A separate `metaharness.io` repository is acceptable only if its access permissions intentionally match the review audience. Do not use a public IO repository for private work.

The same renderer works for Claude Code, Codex, Hermes Agent, or CI because it consumes only a contract and a gate receipt.
