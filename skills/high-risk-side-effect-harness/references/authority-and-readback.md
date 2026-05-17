# Authority and Read-Back Verification

High-risk actions require authority before execution and durable read-back after execution.

## Authority packet

- requester or authorizer
- exact approved action
- target system and identifier
- rollback or irreversibility note
- stop conditions

## Read-back examples

- fetch published URL
- read repository visibility and commit hash
- inspect cron/job definition
- list secret names without values
- verify message target metadata

Never print secret values as part of verification.
