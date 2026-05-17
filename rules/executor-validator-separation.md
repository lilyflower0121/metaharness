# Executor / Validator Separation Rule

For non-trivial work, the executor must not be the final certifier of its own output.

## Minimum separation

- Executor: makes the change or performs the task.
- Evaluator: designs or runs checks.
- Validator: compares the result against the frozen contract and evidence.

## Validation statuses

Use explicit statuses instead of vague success language:

- confirmed
- drift
- regression
- missing_evidence
- blocked

The executor's summary is evidence to inspect, not proof of completion.
