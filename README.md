# metaharness

Metaharness is a public, implementation-neutral repository for codifying harness rules that let AI agents execute tasks autonomously while minimizing user review and deterministically honoring objectives and constraints.

It is based on operational lessons from Hermes Agent, but the artifacts here should stay portable: contracts, rules, schemas, checklists, patterns, examples, and eval cases that can be reused by other agent runtimes.

## Core purpose

Reduce repeated human steering by making the workflow itself enforce:

- frozen task intent
- explicit constraints and non-goals
- evidence-grounded decisions
- side-effect authorization
- executor / evaluator / validator separation
- validation receipts
- disciplined retention of reusable lessons

Metaharness is **not** a prompt dump. It is an architecture for binding agent execution to contracts, evidence, policy gates, validators, and audit receipts.

## Repository map

```text
metaharness/
  principles/   Human-readable design principles
  contracts/    Machine-readable schemas and task packets
  rules/        Normative harness rules
  patterns/     Reusable task pipeline patterns
  checklists/   Preflight, validation, security, release checks
  examples/     Concrete sample harness packets
  evals/        Failure cases and regression scenarios
  docs/         Glossary and design rationale
```

## Initial architecture

The initial architecture is organized as seven layers:

1. Intent Contract Layer
2. Constraint & Policy Layer
3. Evidence & Context Layer
4. Execution Decomposition Layer
5. Validator Compilation Layer
6. Receipt & Audit Layer
7. Retention Layer

See [`docs/architecture.md`](docs/architecture.md).

## Status

Early public scaffold. Interfaces and schema names may change until the first tagged release.
