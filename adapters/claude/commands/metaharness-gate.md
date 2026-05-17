# Metaharness Gate

Run the shared metaharness gate for the provided contract path.

Usage:

```text
/metaharness-gate contracts/examples/merge.medium.valid.yaml
```

Steps:

1. Treat `$ARGUMENTS` as the contract path.
2. Run:

```bash
python3 scripts/run_metaharness.py --contract $ARGUMENTS
```

3. Report pass/fail, validator output, and residual risks.
4. Do not mark the task complete if the command fails.
