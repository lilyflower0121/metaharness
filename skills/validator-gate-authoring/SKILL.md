---
name: validator-gate-authoring
description: Use when converting harness rules, natural-language constraints, or review policies into code-level validators that block gate passage unless risk-appropriate conditions are satisfied.
version: 0.1.0
author: Metaharness Contributors
license: MIT
metadata:
  metaharness:
    risk_tier: meta
    tags: [validators, gates, schemas, policy-as-code, skills]
---

# Validator Gate Authoring

## Overview

Use this skill to turn a harness rule into an enforceable validator. A rule is stronger when the agent cannot pass the gate merely by reading or paraphrasing it.

The output should pair a human-readable SKILL.md with one or more code-level checks: schema validation, static scan, command receipt inspection, path allowlist check, risk-tier gate, or manual-review blocker.

## When to Use

Use when:

- A policy should block completion unless verified.
- A natural-language rule can be expressed as required fields, forbidden fields, path checks, command checks, or receipt checks.
- A user correction reveals that reading instructions is insufficient.
- A public repo needs portable skills plus runnable validation scripts.

## Workflow

1. Classify the rule by risk tier: low, medium, high, or meta.
2. Identify which parts can be enforced by code.
3. Define the contract fields required for that risk tier.
4. Add a validator script or extend an existing gate.
5. Make the SKILL.md point to the exact gate command.
6. Add a positive and negative fixture when possible.
7. Run the validator against the fixtures.
8. Record residual manual-review requirements.

## Validator Design Rules

- Prefer failing closed when a field is missing.
- Keep high-risk gates stricter than medium-risk gates.
- Do not allow the executor summary to satisfy independent validation by itself.
- Do not inspect or print secret values.
- Make errors actionable: say which field failed and why.
- Keep the validator runtime-light so it can run before every gate decision.

## Outputs

- SKILL.md with risk tier and gate command.
- Script or schema implementing the gate.
- Fixture contracts or examples.
- Verification receipt showing pass/fail behavior.

## Common Pitfalls

1. Writing policy prose without a failing test.
2. Making all risk tiers share the same weak requirements.
3. Allowing high-risk actions without authority or rollback fields.
4. Creating validators that depend on a specific private runtime.

## Verification Checklist

- [ ] Skill identifies a risk tier or meta role.
- [ ] Skill names the exact gate command.
- [ ] Validator fails on missing required fields.
- [ ] Validator passes a valid fixture.
- [ ] Validator does not print secrets.
