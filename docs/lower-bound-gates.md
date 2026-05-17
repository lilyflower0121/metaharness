# Lower-Bound (LB) Gates

Metaharness uses risk- and phase-specific gates, but some failures are unacceptable in almost every context. These are the **lower-bound (LB)**: compact, context-independent blockers that must be considered during design and re-checked during validation.

The LB gate is not the full gate. It is the non-negotiable lower bound below every gate.

## Design principle

A task may use a light gate during exploration or MVP work, but it must still not violate the LB.

Examples:

- Exploration can be fast, but it must not leak secrets or perform irreversible side effects.
- MVP work can be incomplete, but it must not silently convert observations into accepted requirements.
- Implementation can be bounded, but it must not edit outside allowed surfaces.
- Release can be automated, but it must not publish without authority and read-back.

## Source families

The LB is synthesized from internal Hermes/metaharness failures and external control families:

- OWASP Top 10 for LLM Applications: prompt injection, sensitive information disclosure, insecure output handling, excessive agency, supply-chain risks.
- OWASP ASVS: testable security requirements and verification rigor rather than intent-only claims.
- NIST SSDF: secure design, secure implementation, verification, vulnerability response.
- CISA Secure by Design: security built into design/defaults rather than added after release.
- NIST AI RMF: govern/map/measure/manage over the lifecycle, with explicit risk context.
- SLSA / OpenSSF: provenance, dependency integrity, automated security posture checks.

## Lower-bound (LB) categories

| ID | Category | Design-stage lower bound | Validation-stage lower bound |
| --- | --- | --- | --- |
| LB-001 | Objective integrity | objective, non-goals, prohibited substitutions are explicit | final receipt does not claim a substitute as success |
| LB-002 | Authority for side effects | external/destructive/account-affecting actions have an authority source or are prohibited | side effects have approval evidence and read-back, or did not occur |
| LB-003 | Data and secret boundary | data classification and external-send policy are explicit | secret/private-data scan or explicit not-applicable reason exists |
| LB-004 | Untrusted input boundary | untrusted/user/web/tool output cannot become instruction without classification | evidence distinguishes direct instruction from untrusted content |
| LB-005 | Allowed surface | allowed paths/tools/services are bounded | changed surfaces/tool use stay inside the bound or stop |
| LB-006 | Evidence over assertion | required evidence sources are named | receipt cites command outputs, paths, URLs, hashes, or review records |
| LB-007 | Stop/rollback | stop conditions and rollback/irreversibility handling are defined | rollback/read-back/irreversibility status is recorded |
| LB-008 | Independent validation threshold | self-pass is not allowed for non-trivial medium/high work | validator identity/result is recorded separately from executor summary |
| LB-009 | Supply-chain baseline | dependency/build/release changes declare provenance expectations | dependency/provenance check or not-applicable reason exists |
| LB-010 | Retention boundary | memory/skill/eval/reference/discard rule is defined | retained lesson has classification and does not store secrets/session noise |

## Contract shape

Every gated contract should include:

```yaml
lower_bound:
  design_controls:
    objective_integrity: "..."
    authority_boundary: "..."
    data_boundary: "..."
    untrusted_input_boundary: "..."
    allowed_surface: "..."
    evidence_lower_bound: "..."
    stop_or_rollback: "..."
    validator_boundary: "..."
    supply_chain_boundary: "... or not_applicable: ..."
    retention_boundary: "..."
  validation_controls:
    evidence_receipt: "..."
    side_effect_readback: "... or not_applicable: ..."
    secret_or_private_data_check: "... or not_applicable: ..."
    changed_surface_check: "..."
    validator_result: "..."
    rollback_or_irreversibility_result: "..."
    retention_result: "..."
```

The script accepts explicit `not_applicable: reason` values. Bare `N/A`, `none`, `TBD`, or empty strings do not pass.

## Executable gate

```bash
python3 scripts/lb_gate.py --contract <contract.yaml>
```

The portable runner executes it before risk/phase-specific validators:

```bash
python3 scripts/run_metaharness.py --contract <contract.yaml>
```

## Design-stage enforcement

The LB is intentionally placed in the contract, not only in the final receipt. This forces the agent to decide before execution:

- what must not happen;
- which data can move where;
- which surfaces can be changed;
- what counts as evidence;
- who/what can authorize side effects;
- what stops the run;
- what will be retained or discarded.

If the LB cannot be filled, the task should remain in exploration or ask for authority/scope clarification instead of proceeding to implementation/release.
