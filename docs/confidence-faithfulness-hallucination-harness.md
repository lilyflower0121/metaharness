# Confidence-faithfulness hallucination harness

Hallucination controls often fail when they treat factuality as a simple `answer` versus `abstain` decision. A stricter abstention threshold can reduce confident errors while also suppressing many useful correct answers. This pattern instead treats hallucinations as **confident unsupported errors** and makes uncertainty a claim-local, evidence-linked, action-driving control signal.

Primary research reference: [Hallucinations Undermine Trust; Metacognition is a Way Forward](https://arxiv.org/abs/2605.01428) (Yona, Geva, Matias; arXiv:2605.01428v1; ICML 2026 Position Track). The paper argues that factuality gains often expand the model's knowledge boundary without reliably improving awareness of that boundary, and proposes **faithful uncertainty**: aligning linguistic uncertainty with intrinsic uncertainty. This harness pattern is an implementation-neutral adaptation of that idea.

## Purpose

Use this pattern when an agent, model, or research workflow produces factual claims that may be consumed by a user, artifact, downstream agent, tool call, decision, or automated action.

The harness should make uncertainty operational rather than cosmetic:

- claim language should match the evidence state;
- unsupported confidence should trigger retrieval, verification, review, or `cannot_harness`;
- low-confidence but low-loss claims may remain usable with scoped caveats;
- high-loss claims require evidence receipts, stronger validators, or abstention;
- downstream artifacts must preserve uncertainty, conditions, and allowed-use boundaries.

## Non-goals

- Do not assume the runtime exposes calibrated internal confidence.
- Do not treat hedging words as safety evidence by themselves.
- Do not make the model useless by replacing every uncertain answer with silence.
- Do not optimize only for fewer wrong answers without measuring utility loss, review cost, and downstream action loss.
- Do not let a confident final answer erase source limits, unresolved conflicts, or missing-critical coverage.

## Core model

For each material claim, record both the claim's evidence state and the cost of being wrong or silent.

```yaml
claim_uncertainty_record:
  claim_id: claim-001
  claim_text: "..."
  output_type: fact | estimate | interpretation | recommendation | requirement | action_permission
  evidence_state: verified | source_grounded | retrieved_unverified | model_only | conflicting | stale | missing
  uncertainty_expression: direct | qualified | estimate_range | hypothesis | unknown | cannot_harness
  language_strength: absolute | strong | moderate | weak | question
  loss_if_wrong: negligible | low | medium | high | critical | catastrophic
  loss_if_silent: negligible | low | medium | high | critical
  action_route: answer | hedge | retrieve | ask_user | escalate_review | abstain | cannot_harness
  allowed_use_scope:
    ideation: true
    draft_generation: true
    internal_human_review: true
    customer_facing_artifact: false
    operational_decision: false
    automated_action: false
```

The harness should treat `model_only + strong/absolute language` as a failure unless the claim is explicitly low-loss and marked as hypothesis or opinion. It should treat `verified/source_grounded + weak language` as possible utility loss when the user needed a direct answer and the loss if wrong is low.

## Gate sequence

### Gate 0: Claim and use-scope declaration

Before validation, decide which claims matter and where the output may be used. A chat answer, report section, code comment, evaluation label, or tool decision can all carry claims. For each material claim, declare:

- intended audience and downstream use;
- whether the claim is factual, interpretive, numeric, prescriptive, or action-authorizing;
- evidence state required for that use;
- loss if wrong, stale, missing, overconfident, or underconfident;
- whether the claim can be recalled or corrected downstream.

### Gate 1: Confidence-faithfulness check

Compare language strength against evidence state and loss:

- `absolute` or `strong` language requires direct verification, admitted primary evidence, or an explicit reviewer receipt for high-loss claims.
- `moderate` language may be acceptable for source-grounded but not independently verified claims if downstream use is limited.
- `weak`, `hypothesis`, or `unknown` language should be used for model-only, conflicting, stale, or incomplete evidence.
- `cannot_harness` is required when the current evidence, authority, tools, or reviewers cannot support the claim or action.

### Gate 2: Uncertainty-to-action routing

Uncertainty should change what the agent does, not only how it writes.

```yaml
uncertainty_to_action_policy:
  verified_low_loss: answer
  source_grounded_medium_loss: answer_with_citation_or_qualifier
  retrieved_unverified_medium_loss: retrieve_or_review_before_strong_claim
  model_only_low_loss: hedge_or_mark_hypothesis
  model_only_medium_plus_loss: retrieve_or_ask_user
  conflicting_high_loss: escalate_review_or_cannot_harness
  stale_operational_claim: refresh_source_before_use
  missing_action_authority: abstain_or_cannot_harness
```

Tool use and retrieval should be triggered by stale knowledge, underspecified scope, high-loss consequences, conflict, missing authority, or requested current facts. Abstention is the right route only when retrieval/review cannot resolve the gap within the contract.

### Gate 3: Utility-tax receipt

Reducing hallucination by refusing too much can be a hidden failure. Record what the harness withheld, hedged, delayed, or routed to review:

```yaml
utility_tax_receipt:
  withheld_claims: 3
  hedged_claims: 5
  retrievals_triggered: 2
  human_reviews_required: 1
  useful_correct_claims_suppressed: unknown
  reason: high-loss operational claims lacked admitted evidence
  mitigation: allow ideation/draft use while blocking operational decision use
```

The receipt helps distinguish safer behavior from avoidable uselessness.

### Gate 4: Downstream preservation

Before a claim feeds a rendered artifact, agent handoff, tool call, release note, dashboard, or decision packet, check that downstream output preserves:

- evidence references and source authority;
- uncertainty and confidence qualifiers;
- applicability limits and exclusions;
- conflict notes and missing-critical coverage;
- allowed-use scope and blocked uses;
- recall path for later correction.

### Gate 5: Evaluation

Do not score only answer correctness. Evaluate confidence and routing:

- wrong-confident rate;
- right-overly-hedged or right-suppressed rate;
- calibration or confidence-bucket reliability when available;
- retrieval/search trigger precision and recall;
- abstention precision and recall;
- downstream expected loss by use case;
- preservation of uncertainty in generated artifacts;
- reviewer load and delay cost.

For ranked source review, use @k metrics; for numeric estimates, use RMSE/MAE/interval coverage; for risk scores, use calibration/Brier/threshold expected loss; for rare high-loss harms, use tail-risk scenarios and human escalation gates.

## Gateable failure modes

- Confident claim without evidence receipt.
- Hedge-only safety: uncertainty wording exists but does not change action route or allowed-use scope.
- Answer-vs-abstain tunnel vision: the system suppresses useful low-loss answers instead of using scoped uncertainty.
- Tool-use undertrigger: the agent answers from memory when the claim is current, stale, underspecified, high-loss, or tool-verifiable.
- Tool-use overtrigger: the agent searches or asks humans for low-loss claims that could be answered with an appropriate qualifier.
- Uncertainty erasure: downstream artifact removes caveats, source limits, conditions, or blocked-use labels.
- Calibration metric overclaim: a good aggregate calibration score hides catastrophic confident errors or bad routing at the operating threshold.

## Minimum viable implementation

A small implementation should include:

1. A claim record schema or checklist with evidence state, language strength, loss-if-wrong, loss-if-silent, action route, and allowed-use scope.
2. A linter or reviewer checklist that flags unsupported strong language and missing `cannot_harness` entries.
3. An uncertainty-to-action policy that routes high-loss uncertainty to retrieval, review, or abstention.
4. A utility-tax receipt that records withheld and hedged material.
5. Negative fixtures for wrong-confident answers, over-abstention, stale-current-fact answers, and uncertainty erasure in downstream artifacts.

## Adoption guidance

In a target repository, treat this document as an `interpret_pattern` unless the target also imports concrete schemas, validators, and fixtures. Do not make this prose the sole gate. Compile the policy into task-specific checks that know the target's source types, claim classes, loss thresholds, retrieval tools, and review authority.
