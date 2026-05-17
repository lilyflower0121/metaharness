#!/usr/bin/env python3
"""Create a starter metaharness artifact-flow contract."""
from __future__ import annotations
import argparse
from pathlib import Path

TEMPLATE = """risk_tier: {risk}
objective: {objective}
non_goals:
  - TBD
prohibited_substitutions:
  - TBD
constraints:
  allowed_paths:
    - TBD
  allowed_tools:
    - TBD
  external_side_effect_policy: {side_effect_policy}
  data_classification: TBD
evidence_policy:
  required_sources:
    - TBD
validation:
  automated_checks:
    - python3 scripts/artifact_flow_gate.py --contract {output}
    - python3 scripts/metaharness_gate.py --risk {risk} --contract {output}
  manual_checks:
    - Review deliverables against objective and non-goals.
  validator_role: independent validator
  success_criteria:
    - Artifact-flow and risk-tier gates pass.
rollback:
  rollback_path: TBD
  irreversible_actions: []
stop_conditions:
  - Required evidence is missing.
artifact_flow:
  artifact_type: {artifact_type}
  target_users:
    - TBD
  deliverables:
    - TBD
  build_steps:
    - TBD
  validators:
    - python3 scripts/artifact_flow_gate.py --contract {output}
    - python3 scripts/metaharness_gate.py --risk {risk} --contract {output}
  acceptance_receipt: TBD
"""

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--risk', choices=['low','medium','high'], required=True)
    ap.add_argument('--objective', required=True)
    ap.add_argument('--artifact-type', default='other')
    ap.add_argument('--output', required=True)
    ns = ap.parse_args()
    side = 'none' if ns.risk == 'low' else ('bounded repository/local changes only' if ns.risk == 'medium' else 'explicit approved side effects only')
    content = TEMPLATE.format(risk=ns.risk, objective=ns.objective, artifact_type=ns.artifact_type, output=ns.output, side_effect_policy=side)
    Path(ns.output).parent.mkdir(parents=True, exist_ok=True)
    Path(ns.output).write_text(content, encoding='utf-8')
    print(ns.output)
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
