# Reversible Change Validation

Medium-risk changes must keep scope bounded and rollback practical.

## Required checks

- list changed files
- verify files are inside allowed paths
- run declared validators/tests
- keep a rollback path such as `git revert <commit>`
- record residual risk in the receipt

## Escalation

Escalate to high risk when a change publishes externally, changes permissions, touches credentials, schedules automation, or is not safely reversible.
