# Coding Pipeline Pattern

Use for non-trivial code changes.

```text
intake/router → frozen contract → codebuilder → codetester → codegate → receipt
```

## Roles

- Intake/router: classifies risk and gathers prerequisites.
- Codebuilder: implements only within the allowed scope.
- Codetester: designs and runs focused checks without trusting the builder summary.
- Codegate: validates the diff, checks, evidence, and residual risks against the contract.

## Required outputs

- changed files
- commands run
- tests/checks and results
- validation status
- residual risks
- rollback path
