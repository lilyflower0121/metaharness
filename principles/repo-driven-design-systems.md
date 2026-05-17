# Repo-driven design systems

## Purpose

This principle covers repositories that want to replace detached design files with a production-synchronized, agent-operable design system. The goal is not to remove human review. The goal is to move the source of truth into the repository while giving humans better review surfaces than a static mock file.

## Core rule

The production repository is the source of truth for product UI:

- design tokens and semantic tokens;
- production components and component APIs;
- Storybook or an equivalent component catalog;
- page and flow previews generated from the app;
- visual, accessibility, interaction, and responsive checks;
- `DESIGN.md`, local agent instructions, design ADRs, and component registries.

Figma or another visual design tool may remain a bridge, sketchpad, or archive, but it must not be the authoritative artifact for components, tokens, or UI review once the migration is complete.

## Human-verifiable review surfaces

A repository-driven design system must remain reviewable by non-implementers. Replace detached design files with generated or repository-attached review surfaces:

```text
/design-system
  /tokens
  /semantic-tokens
  /components
  /patterns
  /pages
  /flows
  /deprecated
```

The review surface should cover the whole stack:

1. **Raw tokens** — color, typography, spacing, radius, shadow, motion, breakpoints, contrast samples.
2. **Semantic tokens** — status, intent, emphasis, focus, disabled, selection, evidence, risk, trust roles.
3. **Primitive components** — variants and states for buttons, inputs, links, badges, icons, text, and other primitives.
4. **Composite components** — cards, dialogs, tables, navigation, form fields, empty states, loading, error, permission, and long-content states.
5. **Patterns** — dashboard, settings, list-detail, wizard, onboarding, search/filter, and error-recovery layouts.
6. **Pages** — real route previews and screenshots at mobile, tablet, and desktop sizes.
7. **Flows** — traces, annotated screenshots, or screen recordings for important journeys.
8. **Deprecated assets** — old components/patterns/pages and their replacements, so retired design assets do not re-enter the product.

## Migration rule

Existing visual-design assets should be inventoried and classified before adoption:

```text
visual design asset -> layer classification -> repo destination -> migrate/map/implement/archive/discard -> human review surface -> retirement evidence
```

Use these layers:

- raw token;
- semantic token;
- primitive component;
- composite component;
- pattern;
- page;
- flow;
- deprecated/archive.

Use these actions:

- `migrate` — move the rule/value into repository-owned tokens, docs, or decisions;
- `map` — connect the visual asset to an existing repository component or page;
- `implement` — build the missing repository-owned component/pattern/page;
- `archive` — preserve as historical reference only;
- `discard` — intentionally reject as stale, unused, unsafe, or off-brand.

The migration is complete only when every asset is resolved by one of those actions. Perfect visual parity with the old design file is not required; the repository design system should represent the current product truth.

## New UI rule

New UI work should proceed from existing repository assets before creating new primitives:

```text
existing component composition
  -> variant addition
  -> composite component addition
  -> primitive component addition
```

A new primitive component is the last resort. If needed, require a proposal that states:

- purpose and user need;
- existing alternatives and why they are insufficient;
- API and props;
- required states and responsive behavior;
- token dependencies;
- accessibility requirements;
- examples and non-goals;
- stories, tests, screenshots, and review evidence to be produced.

## Review evidence rule

A UI/design change is not complete until the review packet includes enough evidence for a human to review without opening the retired design tool:

- Storybook or component catalog URL/path;
- preview URL/path for real pages;
- mobile/tablet/desktop screenshots;
- covered states: normal, empty, loading, error, permission-denied, long-content;
- accessibility result;
- visual regression result;
- token changes;
- new component/primitive declaration;
- deprecated asset impact if relevant.

## Retirement rule

A detached design tool can be retired as source of truth only after operating evidence exists:

- no unresolved tool-only raw tokens, semantic tokens, components, patterns, pages, or flow decisions;
- major production components have repository-owned stories/docs and review states;
- recent UI changes were completed without relying on the detached tool as source of truth;
- reviewers can decide from previews, screenshots, traces, tests, and diff evidence;
- new agents or contributors can perform UI tasks from repository docs and catalogs;
- the old tool is marked read-only/archive and its onboarding links are removed or demoted.

## Harness interpretation

This principle is an `adapt_policy` pattern for target repositories. Do not paste it blindly as binding policy. Translate it into the target repository's own design-system docs, component registry, CI checks, PR templates, and review surfaces. Use the checklist in `checklists/repo-driven-design-system-migration.md` when applying it.
