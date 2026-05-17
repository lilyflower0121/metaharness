# Metaharness IO Publishing

Metaharness IO is a companion publication surface for gate receipts and inspected evidence. It is derived from a metaharness-enabled repository, but it should contain **reviewable outputs**, not the entire working context.

## Purpose

Use IO when humans need to review what an agent did and why a harness gate passed:

- task objective, phase, and risk tier;
- LB / risk / phase / artifact gate results;
- commands that were run and their pass/fail status;
- evidence pointers and validation receipts;
- residual risk and retention notes;
- explicit publication visibility.

The IO surface is intentionally static. A static bundle can be hosted by GitHub Pages, a private repository Pages site, an internal docs server, or attached to a PR/release artifact.

## Visibility model

IO does not make a private review public by itself. Visibility is inherited from where the generated site is hosted.

| Source/work repo | IO host | Who can view |
| --- | --- | --- |
| public repo | public Pages/repo | everyone |
| private repo | private/internal Pages/repo or CI artifact | only people with that access |
| public repo with private evidence | private IO host, public-safe redacted summary only | depends on IO host |

Rule: **never rely on the renderer to enforce access control**. The renderer redacts and blocks obvious leaks, but repository or hosting permissions are the authorization boundary.

## Contract section

A task that will publish IO should add:

```yaml
io_publication:
  visibility: public        # public | private | internal
  audience:
    - maintainers
    - reviewers
  publish_target: docs-site-or-pages-repo
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
    reviewer_role: maintainer_or_authorized_reviewer
```

For public IO, `constraints.data_classification` should be public or explicitly redacted. For private IO, the host repository or artifact store must be private/internal.

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

3. Publish the generated directory through the chosen host:

- public GitHub Pages for public material;
- private repository Pages / internal docs for private material;
- CI artifact for review-only material.

## Required properties

An IO bundle must be:

- **reviewable**: a human can see which gates ran and which evidence was checked;
- **bounded**: it does not dump raw logs or secrets by default;
- **traceable**: links back to contract path, receipt schema, commit, and validator names;
- **visibility-aware**: public/private/internal is explicit;
- **static**: no remote JS, no external analytics, no hidden network calls.

## Non-goals

- IO is not a replacement for access control.
- IO is not a complete audit log for every token or tool call.
- IO does not prove semantic correctness; it publishes gate evidence for review.
- IO should not store credentials, private chat logs, customer data, or full raw terminal dumps unless a private host and explicit authority exist.

## Repository layout options

Recommended patterns:

```text
metaharness/                 # rules, contracts, gates
  scripts/render_io.py
  docs/io-publishing.md

metaharness.io/              # optional derived publication repo
  public/                    # generated static pages
  receipts/                  # sanitized JSON receipts
```

or inside a consuming repo:

```text
some-private-project/
  .metaharness/contracts/
  .metaharness/receipts/
  site/io/                   # generated, hosted privately
```

The same renderer works for Claude Code, Codex, Hermes Agent, or CI because it consumes only a contract and a gate receipt.
