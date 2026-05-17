# Repo-driven Design System Migration

Use this checklist when migrating from detached design-tool assets to a repository-owned, human-verifiable design system.

## 1. Source-of-truth decision

- [ ] The repository names its UI/design source of truth.
- [ ] Detached design tools are classified as bridge, sketchpad, review aid, or archive rather than source of truth.
- [ ] `DESIGN.md`, token files, component registry, Storybook/catalog, page previews, and design ADRs have clear ownership.
- [ ] New UI work is prohibited from starting as a binding detached mock unless an exception is recorded.

## 2. Existing asset inventory

Create or update an inventory like:

```md
| Asset | Layer | Repo destination | Action | Status | Reviewer evidence |
| --- | --- | --- | --- | --- | --- |
| Brand colors | raw token | tokens/color.json | migrate | done | /design-system/tokens |
| Primary Button | primitive component | src/components/Button.tsx | map | in progress | Storybook/Button |
| Pricing Card | composite component | src/components/PricingCard.tsx | implement | pending | pending |
| Old hero page | page | none | discard | deprecated | /design-system/deprecated |
```

Layer values:

- [ ] raw token
- [ ] semantic token
- [ ] primitive component
- [ ] composite component
- [ ] pattern
- [ ] page
- [ ] flow
- [ ] deprecated/archive

Action values:

- [ ] `migrate`
- [ ] `map`
- [ ] `implement`
- [ ] `archive`
- [ ] `discard`

## 3. Human review surfaces

The target repository provides human-readable/browser-reviewable surfaces for:

- [ ] raw tokens: color, text, spacing, radius, shadow, motion, breakpoint samples;
- [ ] semantic tokens: status, intent, emphasis, focus, disabled, risk, evidence, trust roles;
- [ ] primitive components: variants, states, responsive behavior, accessibility notes;
- [ ] composite components: empty, loading, error, permission, long-content, mobile/tablet/desktop states;
- [ ] patterns/layouts: dashboard, settings, list-detail, wizard, onboarding, search/filter, error recovery as applicable;
- [ ] pages/routes: real previews and screenshots at mobile/tablet/desktop widths;
- [ ] flows: traces, annotated screenshots, or recordings for important journeys;
- [ ] deprecated assets: old assets, replacement guidance, and do-not-use notes.

## 4. Figma-only / detached-tool-only count

Before retirement, resolve every detached-tool-only item:

- [ ] raw tokens: 0 unresolved
- [ ] semantic tokens: 0 unresolved
- [ ] primitive components: 0 unresolved
- [ ] composite components: 0 unresolved
- [ ] patterns: 0 unresolved
- [ ] page templates: 0 unresolved
- [ ] flow decisions: 0 unresolved

Resolution can be migrate, map, implement, archive, or discard. It does not have to mean every old asset is implemented.

## 5. Component migration definition of done

For each migrated or mapped component:

- [ ] production component exists or an explicit discard/archive decision exists;
- [ ] props, variants, and states are defined;
- [ ] Storybook or equivalent catalog story exists;
- [ ] default, hover, active, focus, disabled, loading/error/empty states are covered as applicable;
- [ ] long text and realistic data are covered;
- [ ] responsive states are covered;
- [ ] accessibility checks or manual notes exist;
- [ ] visual regression or screenshot evidence exists;
- [ ] token dependencies are repository-owned;
- [ ] usage rules are documented in `DESIGN.md`, component docs, or registry;
- [ ] deprecated alternatives are listed.

## 6. New UI process

New UI work follows this order:

```text
brief -> existing asset check -> reuse decision -> proposal if needed -> implementation -> stories/tests/screenshots -> human review -> catalog update
```

Required brief fields:

- [ ] user / job to be done;
- [ ] goal and success metric;
- [ ] non-goals;
- [ ] data, permission, responsive, and accessibility constraints;
- [ ] existing components/patterns/tokens inspected.

Reuse decision order:

- [ ] existing component composition;
- [ ] variant addition;
- [ ] composite component addition;
- [ ] primitive component addition only with proposal approval.

## 7. New primitive proposal gate

If a new primitive is proposed, the proposal includes:

- [ ] purpose and user need;
- [ ] existing alternatives and why they fail;
- [ ] API/props;
- [ ] states and responsive behavior;
- [ ] token dependencies;
- [ ] accessibility requirements;
- [ ] examples and non-goals;
- [ ] required stories, tests, screenshots, and review evidence;
- [ ] reviewer/owner approval before implementation.

## 8. PR review evidence

Every UI/design PR includes:

- [ ] Storybook/catalog URL or path;
- [ ] page preview URL/path if a route changed;
- [ ] mobile/tablet/desktop screenshots;
- [ ] covered states: normal, empty, loading, error, permission-denied, long-content as applicable;
- [ ] accessibility result;
- [ ] visual regression result;
- [ ] token changes summary;
- [ ] new component/primitive declaration;
- [ ] deprecated asset impact;
- [ ] rollback or revert path.

## 9. Retirement gate

The detached design tool is no longer source of truth only when:

- [ ] all detached-tool-only assets are resolved;
- [ ] major production components have stories/docs and review states;
- [ ] recent UI changes completed without detached-tool dependency;
- [ ] human reviewers can decide from previews, screenshots, traces, test output, and diffs;
- [ ] a new contributor or agent can perform a UI task from repository docs/catalogs;
- [ ] old design files are marked read-only/archive or explicitly deprecated;
- [ ] onboarding and agent instructions point to repository-owned review surfaces.

## 10. Adoption classification

When applying this checklist to a target repository, classify artifacts:

- [ ] `principles/repo-driven-design-systems.md` -> usually `adapt_policy` or `interpret_pattern`;
- [ ] this checklist -> `copy_then_configure` or `adapt_policy`;
- [ ] local token/catalog/preview scripts -> target-specific implementation, not copied from metaharness unless separately provided;
- [ ] old design files -> target-owned inventory, not metaharness evidence.
