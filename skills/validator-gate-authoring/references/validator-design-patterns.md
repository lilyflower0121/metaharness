# Validator Design Patterns

Use these patterns when converting harness prose into code-level gates.

## Structural gate

Checks required fields and fails closed when missing. Example: `scripts/metaharness_gate.py`.

## Artifact-flow gate

Checks that a build flow has deliverables, build steps, validators, and a receipt. Example: `scripts/artifact_flow_gate.py`.

## Static scan

Checks filenames, contents, dependency manifests, or policy-prohibited patterns.

## Receipt gate

Checks that claimed results have evidence, commands, statuses, and residual risks.

## Negative fixture

Every important gate should have at least one fixture that must fail.
