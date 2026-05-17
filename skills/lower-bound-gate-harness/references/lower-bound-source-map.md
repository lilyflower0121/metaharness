# Lower-Bound (LB) Source Map

This reference maps lower-bound metaharness controls to source families.

## Internal patterns

- Repeated Hermes/metaharness feedback: prose-only rules are insufficient; prohibited substitutions and objective drift must be blocked before execution.
- Coding-agent best-practice notes: exploration, planning, execution, verification, review, and checkpointing need different gates, but none should bypass objective/data/authority/evidence boundaries.
- Multimodal/MVP feedback notes: feedback is evidence, not instruction; accepted requirements must be classified before implementation.

## External control families

- OWASP Top 10 for LLM Applications:
  - Prompt injection -> untrusted-input boundary.
  - Sensitive information disclosure -> data/secret boundary.
  - Excessive agency -> authority boundary and allowed surface.
  - Supply-chain vulnerabilities -> dependency/provenance boundary.
- OWASP ASVS:
  - Security requirements should be verifiable, not just declared.
- NIST SSDF:
  - Secure design and verification are lifecycle activities, not final-only review.
- CISA Secure by Design:
  - Default safety properties should be built into the design.
- NIST AI RMF:
  - Govern/map/measure/manage requires explicit context and risk treatment.
- SLSA / OpenSSF Scorecard:
  - Build/release/dependency work needs provenance and automated checks.

## Rule

The LB gate is intentionally compact. It does not replace high-risk security review, but no phase/risk-specific gate may pass below it.
