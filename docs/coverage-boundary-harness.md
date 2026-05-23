# Coverage boundary harness

A coverage result is only meaningful when its denominator is visible. A scoped `pass` can be correct for a pilot claim set while remaining unsafe for domain-wide completeness or service use.

This pattern addresses accidents where a narrow internal-review check is later read as a complete domain, legal, safety, operational, compliance, or service-readiness approval.

## Purpose

Use this pattern when a contract, receipt, report, or downstream artifact may contain a coverage-like pass/fail label. The harness should force readers and validators to know what population was checked and which broader populations were not checked.

The coverage boundary separates four questions:

1. **Coverage denominator** — what population, rows, claims, lenses, cases, or assets were actually counted.
2. **Declared-scope coverage** — whether coverage passed inside that named denominator.
3. **Domain coverage completeness** — whether the broader domain was assessed or remains incomplete/not assessed.
4. **Service-use coverage** — whether the result is sufficient for customer-facing, operational, automated, compliance-grade, or other service use.

## Required contract section

Use a `coverage_boundary` section when any coverage pass could be reused downstream:

```yaml
coverage_boundary:
  denominator:
    id: internal_review_pilot_claim_set_v1
    description: Narrow internal-review pilot claim set, not the full domain.
    includes:
      - admitted pilot rows
      - declared coverage lenses required for internal review
    excludes:
      - full domain completeness
      - service-use readiness
      - responsibility boundaries not supported by evidence

  declared_scope_coverage:
    status: pass
    denominator: internal_review_pilot_claim_set_v1
    missing_blockers: []
    meaning: No missing blockers were found inside the declared pilot denominator only.

  domain_coverage_completeness:
    status: not_assessed
    reason: Full-domain completeness was not evaluated.

  service_use_coverage:
    status: blocked
    reason: Out-of-scope blockers remain material for service use.
    blockers:
      - unresolved responsibility boundary

  out_of_scope_blockers:
    - item: full responsibility boundary
      reason: the pilot evidence does not establish all accountable parties
      acceptable_for_declared_scope: true
      blocks_domain_claim: true
      blocks_service_use: true
      required_escalation: domain owner or legal/operational reviewer receipt

  allowed_claims:
    - Declared pilot-scope coverage passed for the named denominator only.
  forbidden_claims:
    - Domain coverage is complete.
    - Ready for service use.
```

## Rules

- Do not emit a bare `coverage: pass`, `critical_coverage: pass`, or equivalent label unless the nearby receipt names the denominator.
- `declared_scope_coverage: pass` means only that no missing blockers were found inside the declared denominator.
- `domain_coverage_completeness` and `service_use_coverage` are separate decisions. Passing one does not imply passing the others.
- `out_of_scope_blockers` must say whether the blocker is acceptable for the declared scope and whether it blocks domain claims or service use.
- If a renderer, summary, PR body, report, or downstream agent preserves only the word `pass` and drops the denominator, treat that as a failed receipt.

## Gate sequence

### Gate 0: Denominator freeze

Before evaluating coverage, record the counted population and explicit exclusions. If the denominator is unstable or unknown, do not allow a pass label.

### Gate 1: Scope-specific result

Emit the declared-scope result separately from domain and service-use results. A pilot/internal-review pass should be labeled as such.

### Gate 2: Completeness and service-use split

Record whether domain completeness was assessed, failed, passed, or not assessed. Separately record whether service use is allowed, blocked, failed, or not assessed.

### Gate 3: Out-of-scope blocker classification

For every out-of-scope blocker, state whether it is acceptable for the declared scope and whether it blocks domain-wide claims or service use.

### Gate 4: Claim preservation

Record allowed and forbidden claims so downstream summaries cannot launder a scoped pass into a global approval.

## Review checklist

- Does every coverage pass name the denominator it applies to?
- Are domain completeness and service-use coverage separate from pilot/internal-review coverage?
- Are excluded populations visible, not hidden in prose caveats?
- Do out-of-scope blockers say whether they block service use?
- Would a reader know which claims are allowed and forbidden after the gate passes?
- Does the final receipt avoid denominator-free `pass` labels?

## Relationship to scope boundary

`scope_boundary` states what the task/harness is allowed and unable to check. `coverage_boundary` states what population a coverage result counted and prevents that result from being promoted to broader populations.

Use both when a scoped validation result may be reused as evidence for a broader workflow.
