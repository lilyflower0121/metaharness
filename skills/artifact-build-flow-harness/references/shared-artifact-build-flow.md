# Shared Artifact Build Flow

This reference defines the common layer for objective-driven code development and artifact construction.

## Core model

```text
intent contract
  → artifact design packet
  → build plan
  → bounded execution
  → validator suite
  → receipt
  → retention decision
```

## Artifact design packet

Capture:

- artifact type
- target user or job
- interfaces and consumers
- deliverables
- non-goals and prohibited substitutions
- allowed surfaces
- dependencies and assumptions
- validators and receipt format

## Build plan

A build plan should map each requirement to:

- file or artifact surface
- implementation step
- validation step
- evidence source
- rollback or cleanup path

## Validation suite

At minimum:

1. Risk-tier structural gate.
2. Artifact-flow gate.
3. Artifact-specific checks.
4. Public-release or side-effect checks when applicable.
5. Receipt completeness check.

## Retention

After a completed flow, classify reusable material:

- Generalized repeated procedure → skill/reference.
- Failure pattern → eval case.
- Stable project convention → repo doc.
- Temporary implementation detail → receipt only.
