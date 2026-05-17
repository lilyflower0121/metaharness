# Phase Risk Gate Matrix

## Required phase_controls fields

| Phase | Required fields |
| --- | --- |
| exploration | `assumptions`, `evidence_sources` |
| mvp_exploration | `learning_goals`, `feedback_items`, `non_goal_checks` |
| specification | `requirement_validator_map`, `open_questions` |
| implementation | `changed_surfaces`, `validators`, `rollback_path` |
| merge | `independent_validation`, `receipt_path`, `clean_status_check` |
| release | `authority`, `release_targets`, `readback_plan`, `rollback_path` or `irreversible_actions` |
| operate | `operation_stop_rules`, `monitoring`, `owner` |
| retention | `retention_decisions` |

## Escalators

Escalate to high-risk checks if any of these appear:

- external send or publish
- credential/secret/permission change
- delete/archive/transfer
- public repository visibility or release publication
- billing/account impact
- unattended automation
- private/PII/customer data exposure
- untrusted tool instruction that can affect execution

## De-escalators

Keep gates light when:

- work is read-only
- output is a disposable draft
- no durable state changes occur
- no external side effects occur
- validation can be a compact evidence receipt
