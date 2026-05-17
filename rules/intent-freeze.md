# Intent Freeze Rule

Before substantive execution, the agent must identify the task objective, non-goals, constraints, validation criteria, and stop conditions.

## Rule

The agent must not silently reinterpret the objective during execution.

If implementation convenience conflicts with the frozen intent, the agent must either:

1. choose the path that preserves intent, or
2. stop and request authorization for a scope change.

## Required checks

- Objective is stated in the task contract.
- Non-goals are stated or explicitly marked unknown.
- Prohibited substitutions are listed for tasks where near-miss outputs are likely.
- Success criteria are linked to validation checks.
- Stop conditions are present.
