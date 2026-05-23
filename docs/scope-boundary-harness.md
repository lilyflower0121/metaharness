# Scope boundary harness

A harness is only safe when it knows what it does not cover. Every non-trivial task should distinguish the work that is inside the harness from adjacent work that is outside it, and from conditions the harness cannot verify at all.

This pattern addresses accidents where an agent treats a locally valid result as broader approval: a research packet becomes service-grade evidence, a prototype becomes production design, a source check becomes legal/compliance proof, or a successful validator hides an unverified external dependency.

## Purpose

Use this pattern when a task result may be reused, rendered, published, operationalized, delegated, automated, or treated as approval for a broader workflow.

The harness should make four boundaries explicit:

1. **In scope** — what the harness is designed to check.
2. **Out of scope** — nearby work that is deliberately not checked.
3. **Cannot harness** — claims or actions this harness cannot verify with its available evidence, authority, tools, or reviewers.
4. **Escalation path** — what must happen before an out-of-scope or cannot-harness item can be used.

## Required contract section

Use a `scope_boundary` section in task contracts when this pattern applies:

```yaml
scope_boundary:
  in_scope:
    - candidate identity and admitted source traceability for internal review
  out_of_scope:
    - production approval
    - legal, safety, or compliance determination
  cannot_harness:
    - item: real-world correctness outside admitted sources
      reason: the harness has no direct operational telemetry or domain-owner review
      required_escalation: domain reviewer receipt before operational use
  boundary_assumptions:
    - downstream artifacts preserve allowed-use scope and uncertainty fields
  accident_scenarios:
    - local pass is mistaken for unrestricted downstream approval
  escalation_triggers:
    - downstream use requests customer-facing, operational, automated, or compliance-grade permission
```

## Rules

- A validator pass is scoped evidence, not global truth.
- `out_of_scope` is not a backlog. It is a warning label for what the current task result must not be used to justify.
- `cannot_harness` is stronger than out-of-scope: it names claims/actions that the current harness cannot verify even if the agent works harder inside the same scope.
- If downstream use needs an out-of-scope or cannot-harness item, create a new contract with the missing authority, evidence, tools, reviewers, or operational telemetry.
- Do not let a later renderer, report, PR, release note, or agent summary strip the boundary fields.

## Gate sequence

### Gate 0: Boundary freeze

Before execution, record the in-scope checks, out-of-scope adjacent work, cannot-harness items, assumptions, and escalation triggers.

### Gate 1: Evidence-to-boundary map

For each success criterion, record the evidence class it can actually support. If the evidence only proves structure, reachability, source identity, or local behavior, do not phrase the success criterion as semantic, operational, legal, or production approval.

### Gate 2: Accident scenario review

Name at least one plausible misuse path for medium/high risk work. Examples include local proof being reused as production approval, a human-readable report losing caveats, or a delegated worker inheriting broader authority than the parent contract allowed.

### Gate 3: Cannot-harness escalation

Every cannot-harness item needs a required escalation: reviewer, external system read-back, operational telemetry, stronger source class, legal/security approval, or a separate contract.

### Gate 4: Preservation check

Before completion, verify that final receipts and downstream artifacts preserve the boundary statement. A successful run should say both what passed and what remains unverified.

## Review checklist

- Does the contract say what the harness checks and what it does not check?
- Are cannot-harness items explicit, not hidden as caveats in prose?
- Would a downstream user know which uses remain blocked even after the validator passes?
- Are accident scenarios written from the likely misuse path, not from the happy path?
- Is there a concrete escalation route for each cannot-harness item?
- Does the final receipt preserve the boundary instead of claiming broad completion?

## Relationship to existing layers

- Intent contract: boundary fields prevent objective drift and prohibited substitutions.
- Constraint and policy: boundary fields make unavailable authority, tools, data, and reviewers visible.
- Evidence and context: boundary fields prevent weak evidence from being promoted into stronger claims.
- Validator compilation: `scripts/scope_boundary_gate.py` can check that the boundary section exists and is not empty.
- Receipt and audit: final receipts should include the same boundary, especially residual cannot-harness items.
