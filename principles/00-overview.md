# Metaharness Principles Overview

Metaharness is built around eight initial principles.

## 1. Freeze intent before execution

The task objective, non-goals, success criteria, and stop conditions should be explicit before substantive work begins.

## 2. Treat constraints as first-class inputs

Constraints are not hints. They are part of the task contract and must be preserved through planning, execution, and validation.

## 3. User review is a scarce resource

The harness should absorb routine investigation, verification, formatting, and evidence collection. Ask the user only for decisions that materially change scope, authority, risk, or trade-offs.

## 4. Evidence beats confidence

A model's confidence is weaker than direct evidence. Claims about completion, correctness, safety, or compliance require supporting evidence.

## 5. Executor cannot self-certify

For non-trivial work, implementation and final validation should be separated. The builder's summary is input to validation, not proof.

## 6. Side effects require authority

External sends, publishing, deletion, credential changes, account-affecting actions, and unattended automation require an authority source, rollback path, and verification.

## 7. Lessons must be classified before retention

Not every lesson belongs in always-loaded memory or global rules. Retain facts, skills, evals, references, receipts, or nothing according to durability and reuse value.

## 8. Repository artifacts should be human-verifiable

When a repository replaces an external or detached source of truth, it must provide review surfaces that humans can inspect without trusting agent summaries. For UI/design systems, see [`repo-driven-design-systems.md`](repo-driven-design-systems.md): tokens, components, pages, flows, visual checks, accessibility evidence, and deprecated assets should be visible from repository-owned catalogs or previews.
