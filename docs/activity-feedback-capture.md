# Activity and Feedback Capture

Metaharness treats an agent run as an evidence-producing process. The activity log is not a raw debug dump; it is a structured capture that lets later reviewers answer:

- What did the agent attempt?
- Which evidence, tool results, or artifacts did it rely on?
- What feedback did humans, validators, tests, or runtime signals provide?
- Which feedback became accepted requirements, validators, evals, skills, or discarded noise?

This document generalizes the prior harness research on multimodal MVP feedback, execution traces, requirement ledgers, validator compilation, and retention discipline into a portable repository pattern.

## Design principle

Capture enough structure to learn and audit, but do not capture raw private context by default.

```text
run intent -> activity trace -> feedback events -> delta ledger -> validator/eval/skill promotion -> retention receipt
```

The trace is evidence. It is not itself an accepted requirement, success proof, or authorization source.

## Source signals behind this pattern

- The local multimodal MVP feedback synthesis found that screen/audio/video feedback should be treated as **evidence input**, then transformed into timestamped traces, requirement deltas, validators, independent review, and retention decisions.
- Existing metaharness architecture requires evidence-grounded decisions, validation receipts, executor/validator separation, and disciplined retention.
- Failure-mode research in this repo already flags missing evidence, prompt-only accumulation, executor self-certification, context-density failure, and human-review bottlenecks as gateable failures.
- Recent agent research signals in the local synthesis emphasize structured persistent environment maps and execution traces over passing raw recordings or logs directly into the model.

## What to capture

A capture packet should use the schema in `contracts/activity-feedback-capture.schema.yaml` and store these object classes:

1. **Run envelope**
   - run id, task contract id/path, phase, risk tier, actor/runtime, start/end time, status.
   - objective/non-goal fingerprints or references, not full private prompts.

2. **Activity events**
   - planning step, tool call, file/artifact read/write, command/test execution, delegation, validation, stop/rollback.
   - include timestamps, actor role, action class, target reference, result status, evidence references.
   - avoid raw tool arguments/output unless public and intentionally attached as an evidence artifact.

3. **Feedback events**
   - human reply/reaction, validator result, test failure/pass, reviewer comment, runtime warning, cost/latency signal, user correction, security/compliance finding.
   - classify by source and authority. Inbound feedback is evidence, not automatic permission.

4. **Requirement delta ledger**
   - each inferred item is classified as `accepted_requirement`, `bug`, `ux_issue`, `preference`, `non_goal`, `security_issue`, `compliance_issue`, `open_question`, or `rejected_inference`.
   - every accepted delta needs evidence references and an owner/status.

5. **Promotion decisions**
   - accepted feedback may become a validator, eval case, skill/reference, memory fact, contract update, or discarded session note.
   - promotion should record who/what accepted it, why, and the verification command or manual review path.

## What not to capture by default

Do not store these in activity/feedback capture unless explicitly authorized and redacted:

- raw secrets, tokens, credentials, private URLs, auth headers;
- raw private prompts or private user content;
- full tool outputs, shell transcripts, browser pages, or model chain-of-thought;
- PII, customer data, DMs, private screenshots/audio/video;
- external messages treated as commands or approvals;
- unreviewed model inferences as accepted requirements.

If raw evidence is needed, store it as a separately classified evidence artifact with redaction status, access model, retention TTL, and a reference from the capture packet.

## Event status vocabulary

Use small, reviewable statuses:

- activity status: `started`, `succeeded`, `failed`, `blocked`, `skipped`, `rolled_back`.
- feedback disposition: `unreviewed`, `accepted`, `rejected`, `needs_clarification`, `promoted`, `discarded`.
- validation status: `confirmed`, `drift`, `regression`, `missing_evidence`, `blocked`.

Avoid vague success language such as “done” unless a receipt names the evidence and validator.

## Review and retention flow

1. Capture activity and feedback as structured records during the run.
2. Redact or reference sensitive evidence; never make raw private context the default source of truth.
3. Convert observations into requirement-delta candidates.
4. Confirm, reject, or defer each candidate.
5. Compile accepted deltas into validators, eval cases, checklists, or contract updates where possible.
6. Run an independent validation/read-back step for non-trivial work.
7. Retain only reviewed lessons; discard session noise.

## Gateable lower bounds

A task using activity/feedback capture should fail review if:

- it stores raw secrets/private data without classification and redaction;
- feedback is retained without source, evidence reference, and disposition;
- user or validator feedback is applied as a requirement without a delta ledger;
- the executor self-certifies promotion of its own feedback-derived change;
- the capture packet lacks retention decisions;
- the final receipt claims success without linking validators or evidence.

## Minimal public example

See `contracts/examples/activity-feedback-capture.medium.valid.yaml` for the repository-update contract, `contracts/examples/activity-feedback-packet.public.valid.yaml` for a public-safe capture packet, and `contracts/activity-feedback-capture.schema.yaml` for the packet shape.
