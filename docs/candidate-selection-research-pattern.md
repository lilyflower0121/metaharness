# Candidate selection research subpattern

Some research tasks do not produce a single answer. They produce candidate items that may later be selected, cited, rendered, operationalized, or rejected.

This subpattern extends the research task metaharness for those tasks. It keeps discovery separate from approval: finding a plausible candidate is not enough to authorize downstream use.

## Purpose

Use this subpattern when a research task returns candidate items that need later human review, ranking, filtering, citation, recommendation, or automated selection.

The subpattern should answer four questions for each material candidate:

1. What is the candidate claimed to be?
2. What evidence supports that identity and applicability?
3. What nearby candidates could be confused with it?
4. For which downstream uses is it currently allowed?

## Non-goals

- Do not encode domain-specific object taxonomies in this public pattern.
- Do not treat a search hit, title match, benchmark row, or summary as approval.
- Do not collapse discovery, identity resolution, evidence admission, and use permission into one pass/fail label.
- Do not make this pattern the source of truth for a target repository's domain policy; adapt it through that repository's own rules and validators.

## Candidate record

Each candidate admitted beyond discovery should be represented as a structured record, not only prose.

```yaml
candidate_record:
  candidate_id: stable-within-packet
  claimed_identity:
    name: example candidate name
    normalized_name: canonical candidate name if known
    aliases: []
    version_or_context: optional bounded context
  identity_basis:
    distinguishing_features: []
    unresolved_identity_risks: []
    confidence: low|medium|high
  evidence:
    source_refs: []
    source_authority: primary|official|vendor|recognized_reference|secondary|unverified
    freshness_or_version: retrieval date, version, or staleness note
    applicability_limits: []
    missing_evidence: []
  confusable_cases:
    - candidate_or_class: nearby but non-equivalent item
      why_confusable: shared names, features, metrics, source wording, or other overlap
      why_not_equivalent: boundary that prevents substitution
      misuse_loss: negligible|low|medium|high|critical
  allowed_use_scope:
    search_index: true
    ideation: true
    draft_generation: true
    internal_human_review: true
    customer_facing_artifact: false
    operational_decision: false
    automated_selection: false
    compliance_grade_assertion: false
  reviewer_questions: []
```

## Gate sequence

### Gate 0: Selection-use contract

Before collecting candidates, freeze the intended downstream use:

- whether the output is for search, triage, drafting, recommendation, decision support, or automation;
- acceptable opportunity loss from rejecting a useful candidate;
- loss if a wrong, stale, non-applicable, or ambiguous candidate is accepted;
- whether reviewers need top-k rankings, one approved candidate, a negative list, or a coverage set;
- prohibited substitutions and contexts where similarity is insufficient.

### Gate 1: Candidate discovery

Collect candidates broadly enough for the intended use, but label this phase as discovery only. Discovery records may be incomplete and should not be used for high-loss downstream actions.

### Gate 2: Identity and applicability resolution

For candidates that may be used beyond ideation, record normalized identity, aliases, version/context, distinguishing features, unresolved identity risks, and applicability limits.

### Gate 3: Evidence admission

Map each material candidate claim to admitted source references. Source count alone is insufficient; the record should say why each source is applicable and what it cannot prove.

### Gate 4: Confusable-case check

List nearby candidates, names, classes, versions, or contexts that could be mistaken for the candidate. At least one negative or boundary case should be included when misuse loss is medium or higher.

### Gate 5: Use-scope decision

Emit `allowed_use_scope` rather than a generic pass/fail. A candidate can be acceptable for search or internal review while blocked from customer-facing, operational, automated, or compliance-grade use.

### Gate 6: Preservation into downstream artifacts

When a downstream artifact consumes a candidate record, verify that identity limits, missing evidence, confusable cases, and use-scope restrictions were not stripped or broadened.

## Metric selection

Select metrics by the downstream selection action:

- ranked review: precision@k, recall@k, nDCG@k, MRR, expected value@k;
- one approved candidate: false-accept cost, reviewer burden, threshold-specific expected loss;
- coverage set: recall of required categories, missing-critical coverage, duplicate or near-duplicate rate;
- numeric comparison: RMSE, MAE, interval coverage, calibration, or threshold loss;
- high-loss acceptance: tail-risk scenarios, negative fixtures, and human escalation.

Do not use search relevance, surface similarity, or count of found candidates as a universal proxy for downstream value.

## Review checklist

- Is discovery clearly separated from approval?
- Does each material candidate have identity, evidence, applicability, and missing-evidence fields?
- Are confusable or non-equivalent nearby candidates recorded when misuse loss is meaningful?
- Is the allowed-use scope narrower than the evidence when uncertainty remains?
- Can downstream artifacts preserve the candidate's limits and recall dependent uses if the record is later rejected?

## Retention

Retain only reviewed, portable lessons:

- reusable candidate schema or validator fixtures in this repository;
- target-domain candidate records in the target repository or dataset;
- recurring false-accept or false-reject cases as evals or negative fixtures;
- one-off candidate searches as task receipts only.
