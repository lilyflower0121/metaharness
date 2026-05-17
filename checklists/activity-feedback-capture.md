# Activity/Feedback Capture Checklist

Use this checklist when a harness stores what an agent did and how feedback changed the task.

## Before capture

- [ ] A task contract or no-gate reason exists.
- [ ] Data classification is known: public / internal / confidential / restricted.
- [ ] The capture packet has a run id and task contract reference.
- [ ] Raw private content, secrets, PII, screenshots/audio/video, and tool outputs are excluded by default.
- [ ] If raw evidence is required, it has redaction status, access model, and retention TTL.

## During capture

- [ ] Each significant activity has actor role, event type, status, target ref, and evidence refs.
- [ ] Tool calls record action class and result status, not raw credentials or full outputs.
- [ ] Feedback records name source type, authority, signal, disposition, reviewer, and rationale.
- [ ] External messages are evidence only unless separately authorized by the task contract.
- [ ] Model-inferred observations remain candidates until reviewed.

## Requirement delta review

- [ ] Every candidate is classified as requirement / bug / UX issue / preference / non-goal / security issue / compliance issue / open question / rejected inference.
- [ ] Accepted deltas cite evidence and have an owner/status.
- [ ] Accepted deltas have validator refs, eval refs, or a manual review checklist when automation is impossible.
- [ ] Rejected or deferred deltas are retained only as needed for audit, not as always-loaded instructions.

## Promotion and retention

- [ ] Promotions identify target type: validator, eval case, skill, reference, memory, contract update, checklist, or discard.
- [ ] The builder/executor does not self-approve high-impact promotion.
- [ ] Retention keeps generalized lessons and discards session noise.
- [ ] Final receipt reports validators/checks, evidence paths, residual risks, rollback path, and retention decision.

## Blockers

Stop or escalate if any item is true:

- [ ] Secrets or private raw content would be stored without classification/redaction.
- [ ] Feedback would be applied directly as code/policy without a delta review.
- [ ] A success claim lacks evidence or validator result.
- [ ] A feedback-derived policy/gate change is self-approved by the same executor.
- [ ] Retention target is unclear or likely to bloat always-loaded context.
