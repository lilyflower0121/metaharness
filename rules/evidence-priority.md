# Evidence Priority Rule

Agent decisions must be grounded in the strongest available evidence.

## Priority order

1. Explicit current user instruction
2. Repository files and project-local instructions
3. Command outputs, tests, logs, and durable system state
4. Approved contracts, receipts, skills, and documented memory
5. External sources with cited URLs or paths
6. Model inference or analogy

Lower-priority evidence must not override higher-priority evidence.

## Rule

The agent should distinguish verified facts from assumptions and should not report success without evidence from tests, checks, read-back verification, or an equivalent receipt.
