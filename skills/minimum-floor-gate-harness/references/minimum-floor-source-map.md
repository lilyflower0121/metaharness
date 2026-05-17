# Minimum Floor Source Map

This reference maps lower-bound metaharness controls to source families.

## Internal patterns

- Repeated Hermes/metaharness feedback: prose-only rules are insufficient; prohibited substitutions and objective drift must be blocked before implementation.
- Coding-agent best-practice synthesis: Explore → Plan → Code → Verify → Review → Checkpoint; verification is required before completion.
- Critical review of metaharness: structural gates are useful but must add evidence/read-back, risk escalation, transition receipts, and semantic validators.
- Multimodal MVP harness research: raw feedback is evidence, not accepted requirement; privacy/security gates remain separate from UX feedback.

## External source families

- OWASP Top 10 for LLM Applications: prompt injection, sensitive information disclosure, excessive agency, insecure output handling, supply-chain vulnerabilities.
- OWASP ASVS: requirements for secure development and verification; controls must be testable.
- NIST SSDF: secure software should be prepared, protected, produced, and respond to vulnerabilities; design must include security, not only final scan.
- CISA Secure by Design: security should be built into product design and defaults.
- NIST AI RMF: governance, mapping, measurement, and management across the lifecycle.
- SLSA: artifact integrity/provenance in build/release chains.
- OpenSSF Scorecard: automated checks for OSS security posture.

## Derived lower-bound rule

If a control failure could cause objective substitution, unauthorized side effects, data leakage, untrusted instruction capture, unbounded blast radius, unverifiable completion, or unsafe retention, it belongs in the minimum floor rather than only in a later specialized gate.
