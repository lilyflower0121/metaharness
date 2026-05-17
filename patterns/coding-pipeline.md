# Coding Pipeline Pattern

Use for non-trivial code changes.

```text
intake/router → frozen contract → codebuilder commit → codetester → codegate → commit receipt → branch/PR aggregate gate
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

## Commit-scoped delegation

For agent-authored changes, prefer one logical change per Git commit. Each commit should be treated as an audit checkpoint with:

- commit/tree/parent hash receipt;
- inferred risk and impact escalators from changed paths and diff contents;
- targeted validators selected by risk;
- test-weakening review when tests change;
- independent codegate verdict before relying on the receipt.

Do not stop at per-commit checks. The branch/PR aggregate gate must recompute cumulative risk, verify receipt/hash integrity after rebase or squash, inspect the final whole diff, and run broader integration/security checks when risk requires.

See `docs/commit-scoped-agent-delegation.md`.
