# Repo-driven Design System Migration

This document explains how to convert detached visual design assets into a repository-owned design system that agents can use and humans can review. It is intended for target repositories that want to retire Figma or another design tool as the source of truth while preserving design quality and reviewability.

## Decision frame

A design migration is successful only when the repository can answer these questions without opening the old design tool:

- What are the canonical tokens and semantic roles?
- Which production components exist, what APIs/states do they support, and when should they be used?
- What page and flow patterns are approved?
- How can a human reviewer inspect tokens, components, pages, flows, edge cases, and regressions?
- Which old assets are deprecated, archived, discarded, or replaced?

The repository is the source of truth. The review surface is generated from or attached to the repository. The old design tool may remain as an archive or bridge, but it is not the authority.

## Recommended artifact stack

```text
repo/
  DESIGN.md                         # agent-readable visual rules and token rationale
  AGENTS.md or local resolver         # agent rules for UI work
  tokens/                             # raw and semantic token files
  src/components/ or packages/ui/      # production components
  src/patterns/                       # reusable layouts and composites
  design/decisions/                   # design ADRs
  design/inventory/                   # detached-tool migration inventory
  design/reviews/                     # review receipts when useful
  tests/visual/                       # screenshot or visual regression specs
  tests/a11y/                         # accessibility checks
  tests/flows/                        # journey tests or traces
```

A target repository may use different paths, but the responsibilities should remain explicit.

## Human review surface stack

Use generated or repository-attached pages, Storybook/Ladle/Histoire, static preview routes, CI artifacts, or same-repository IO pages to expose:

```text
/design-system/tokens
/design-system/semantic-tokens
/design-system/components
/design-system/patterns
/design-system/pages
/design-system/flows
/design-system/deprecated
```

These surfaces replace the old habit of reviewing a detached mock file. They should be easy for non-implementers to inspect.

## Migration stages

### 1. Inventory

List old design assets and classify them by layer and action.

Layers:

- raw token;
- semantic token;
- primitive component;
- composite component;
- pattern;
- page;
- flow;
- deprecated/archive.

Actions:

- `migrate` into repository tokens/docs/decisions;
- `map` to an existing repository component or page;
- `implement` as a missing repository-owned asset;
- `archive` as non-authoritative historical reference;
- `discard` as stale, unused, unsafe, or off-brand.

### 2. Build review surfaces

Before declaring progress, make the migrated materials visible to humans:

- token swatches and contrast examples;
- semantic status/intent/emphasis/focus samples;
- primitive component stories with states;
- composite stories with realistic edge cases;
- pattern examples with data density and responsive behavior;
- page screenshots for mobile/tablet/desktop;
- flow traces or annotated screenshots for important journeys;
- deprecated asset list with replacements.

### 3. Close detached-tool-only gaps

Track unresolved items until each layer reaches zero unresolved detached-tool-only assets. Zero unresolved does not mean every old asset is implemented; it means every old asset has a decision.

### 4. Run repository-native UI work

For new UI, use this order:

```text
brief
  -> existing asset check
  -> existing component composition
  -> variant addition if needed
  -> composite component addition if needed
  -> primitive proposal only as last resort
  -> implementation
  -> stories/tests/screenshots
  -> human review
  -> catalog update
```

### 5. Retire the old source

Retirement requires operating evidence, not only a migration note:

- recent UI changes completed without relying on the old tool as authority;
- reviewers could decide from repo previews, screenshots, traces, tests, and diffs;
- new contributors or agents could perform UI work from repository docs/catalogs;
- old files are marked read-only/archive or deprecated;
- onboarding points to repository-owned sources.

## Agent requirements for UI work

Agents should be required to:

- read `DESIGN.md`, agent instructions, component registry, and relevant stories before writing UI;
- reuse existing components before creating variants or new components;
- avoid one-off colors, spacing, typography, and layout primitives;
- propose a new primitive before implementing it;
- update stories, tests, screenshots, and review evidence with any UI change;
- report preview paths, screenshots, accessibility status, visual regression status, and residual risks.

Agents should be forbidden from claiming completion based only on prose or model confidence.

## Validation and receipts

For target repositories, the final migration or retirement receipt should include:

- inventory path and status counts;
- token and component catalog paths;
- preview or Storybook paths;
- visual/a11y/flow check status;
- unresolved exceptions and owners;
- evidence that recent UI work did not require the old design tool;
- rollback/reopen path if reviewers discover a missing asset.

Use `checklists/repo-driven-design-system-migration.md` as the manual gate. If the target repository implements deterministic validators, record them in the target repository's adoption packet rather than treating this document as executable proof.

## Adoption class

For repository adoption, this document is usually `interpret_pattern` or `adapt_policy`. The checklist may be `copy_then_configure`. Actual token catalogs, preview generators, Storybook configuration, visual regression scripts, and PR templates are target-specific.
