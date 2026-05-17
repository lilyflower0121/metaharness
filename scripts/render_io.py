#!/usr/bin/env python3
"""Render a human-reviewable static Metaharness IO bundle.

The renderer consumes a task contract plus a JSON receipt produced by
`scripts/run_metaharness.py --json`. It writes static, escaped HTML plus sanitized
JSON files. It does not publish to a remote host; repository permissions are the
access-control boundary. IO contracts must use access_model=repository_inherited.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

from yaml_compat import load_path

ROOT = Path(__file__).resolve().parents[1]
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\b(?:ghp|github_pat|sk|xox[baprs])-[-_A-Za-z0-9]{12,}"),
    re.compile(r"\b(?:password|passwd|token|secret|api[_-]?key)\s*[:=]\s*[^\s<>'\"]+", re.I),
]
LOCAL_PATH_PATTERN = re.compile(r"/(?:Users|Volumes|home|var|private|tmp)/[^\s<>'\"]+")


def fail(msg: str) -> int:
    print(f"IO RENDER FAIL: {msg}", file=sys.stderr)
    return 1


def flatten(x: Any) -> str:
    if isinstance(x, dict):
        return "\n".join(f"{k}: {flatten(v)}" for k, v in x.items())
    if isinstance(x, list):
        return "\n".join(flatten(v) for v in x)
    return "" if x is None else str(x)


def redact_text(text: str) -> str:
    text = LOCAL_PATH_PATTERN.sub("[REDACTED_LOCAL_PATH]", text)
    for pat in SECRET_PATTERNS:
        text = pat.sub("[REDACTED_SECRET]", text)
    return text


def sanitize(obj: Any) -> Any:
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            lk = str(k).lower()
            if any(s in lk for s in ["secret", "token", "password", "credential", "private_key"]):
                out[k] = "[REDACTED_FIELD]"
            else:
                out[k] = sanitize(v)
        return out
    if isinstance(obj, list):
        return [sanitize(v) for v in obj]
    if isinstance(obj, str):
        return redact_text(obj)
    return obj


def scan_for_blockers(obj: Any) -> list[str]:
    text = flatten(obj)
    errors = []
    for pat in SECRET_PATTERNS:
        if pat.search(text):
            errors.append(f"secret-like pattern detected: {pat.pattern}")
    return errors


def list_items(values: Any) -> str:
    if not values:
        return "<li><em>none recorded</em></li>"
    if not isinstance(values, list):
        values = [values]
    return "\n".join(f"<li>{html.escape(str(v))}</li>" for v in values)


def render_html(contract: dict[str, Any], receipt: dict[str, Any], generated_at: str) -> str:
    pub = contract.get("io_publication", {})
    validators = receipt.get("validators", [])
    rows = []
    for v in validators:
        cmd = " ".join(v.get("command", [])) if isinstance(v.get("command"), list) else str(v.get("command", ""))
        status = v.get("status", "unknown")
        stdout = v.get("stdout", "")
        stderr = v.get("stderr", "")
        rows.append(
            "<tr>"
            f"<td><span class='status {html.escape(str(status))}'>{html.escape(str(status).upper())}</span></td>"
            f"<td><code>{html.escape(cmd)}</code></td>"
            f"<td><details><summary>output</summary><pre>{html.escape(stdout)}\n{html.escape(stderr)}</pre></details></td>"
            "</tr>"
        )
    lb = contract.get("lower_bound") or contract.get("minimum_floor") or {}
    design = lb.get("design_controls", {}) if isinstance(lb, dict) else {}
    validation = lb.get("validation_controls", {}) if isinstance(lb, dict) else {}
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Metaharness IO Receipt</title>
  <style>
    :root {{ color-scheme: light dark; --ok:#0a7f3f; --bad:#b42318; --muted:#667085; --line:#d0d5dd; }}
    body {{ font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 2rem; line-height: 1.5; max-width: 1100px; }}
    header {{ border-bottom: 1px solid var(--line); margin-bottom: 1.5rem; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; }}
    .card {{ border: 1px solid var(--line); border-radius: 12px; padding: 1rem; }}
    .status.pass {{ color: var(--ok); font-weight: 700; }} .status.fail {{ color: var(--bad); font-weight: 700; }}
    table {{ border-collapse: collapse; width: 100%; }} th, td {{ border: 1px solid var(--line); padding: .6rem; vertical-align: top; }}
    code, pre {{ white-space: pre-wrap; overflow-wrap: anywhere; }} .muted {{ color: var(--muted); }}
  </style>
</head>
<body>
<header>
  <h1>Metaharness IO Receipt</h1>
  <p class="muted">Generated {html.escape(generated_at)}. Static review artifact; repository permissions define who can view it.</p>
</header>
<section class="grid">
  <div class="card"><strong>Status</strong><br><span class="status {html.escape(str(receipt.get('status', 'unknown')))}">{html.escape(str(receipt.get('status', 'unknown')).upper())}</span></div>
  <div class="card"><strong>Phase / Risk</strong><br>{html.escape(str(receipt.get('phase') or contract.get('phase')))} / {html.escape(str(receipt.get('risk_tier') or contract.get('risk_tier')))}</div>
  <div class="card"><strong>Access Model</strong><br>{html.escape(str(pub.get('access_model', 'unspecified')))}</div>
  <div class="card"><strong>Contract</strong><br><code>{html.escape(str(receipt.get('contract', 'unknown')))}</code></div>
</section>
<section>
  <h2>Objective</h2>
  <p>{html.escape(str(contract.get('objective', '')))}</p>
  <h3>Non-goals</h3><ul>{list_items(contract.get('non_goals'))}</ul>
  <h3>Prohibited substitutions</h3><ul>{list_items(contract.get('prohibited_substitutions'))}</ul>
</section>
<section>
  <h2>Publication Policy</h2>
  <div class="grid">
    <div class="card"><strong>Audience</strong><ul>{list_items(pub.get('audience'))}</ul></div>
    <div class="card"><strong>Include</strong><ul>{list_items(pub.get('include'))}</ul></div>
    <div class="card"><strong>Redact</strong><ul>{list_items(pub.get('redact'))}</ul></div>
    <div class="card"><strong>Target</strong><br>{html.escape(str(pub.get('publish_target', 'unspecified')))}</div>
  </div>
</section>
<section>
  <h2>Validator Results</h2>
  <table><thead><tr><th>Status</th><th>Command</th><th>Output</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
</section>
<section>
  <h2>Lower-Bound Design Controls</h2>
  <ul>{list_items([f'{k}: {v}' for k, v in design.items()])}</ul>
  <h2>Lower-Bound Validation Controls</h2>
  <ul>{list_items([f'{k}: {v}' for k, v in validation.items()])}</ul>
</section>
<section>
  <h2>Review Checklist</h2>
  <ul>
    <li>Does the status match the validator outputs?</li>
    <li>Is the IO access model repository_inherited and target repository-synchronized?</li>
    <li>Are side effects backed by authority and read-back?</li>
    <li>Are residual risks and retention boundaries acceptable?</li>
  </ul>
</section>
<footer class="muted">
  <p>Files: <code>receipt.json</code>, <code>contract.redacted.json</code>. This page contains escaped static content only.</p>
</footer>
</body>
</html>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description="Render a static Metaharness IO review bundle")
    ap.add_argument("--contract", type=Path, required=True)
    ap.add_argument("--receipt", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--allow-failed", action="store_true", help="Render failed receipts for private debugging only")
    args = ap.parse_args()

    contract_path = args.contract if args.contract.is_absolute() else ROOT / args.contract
    receipt_path = args.receipt if args.receipt.is_absolute() else ROOT / args.receipt
    out_dir = args.out if args.out.is_absolute() else ROOT / args.out

    try:
        contract = load_path(contract_path)
        receipt = json.loads(receipt_path.read_text())
    except Exception as exc:
        return fail(f"cannot load inputs: {exc}")
    if not isinstance(contract, dict) or not isinstance(receipt, dict):
        return fail("contract and receipt must be mappings")

    pub = contract.get("io_publication")
    if not isinstance(pub, dict):
        return fail("contract missing io_publication section")
    access_model = str(pub.get("access_model", "")).lower()
    if access_model != "repository_inherited":
        return fail("io_publication.access_model must be repository_inherited")
    if "visibility" in pub:
        return fail("io_publication.visibility is not allowed; IO access must inherit repository permissions")
    target = str(pub.get("publish_target", "")).lower()
    allowed_targets = {"same_repository_pages", "same_repository_artifact", "repository_attached_artifact"}
    if target not in allowed_targets:
        return fail("io_publication.publish_target must be repository-synchronized")
    audience = pub.get("audience")
    if not isinstance(audience, list) or "repository_readers" not in {str(x) for x in audience}:
        return fail("io_publication.audience must include repository_readers")
    if receipt.get("status") != "pass" and not args.allow_failed:
        return fail("receipt status is not pass; use --allow-failed only for repository-internal debugging")
    redactions = {str(x).lower() for x in pub.get("redact", [])} if isinstance(pub.get("redact"), list) else set()
    if not {"private_data", "secrets", "absolute_local_paths"}.issubset(redactions):
        return fail("IO publication must redact secrets, private_data, and absolute_local_paths")
    blockers = scan_for_blockers(contract) + scan_for_blockers(receipt)
    if blockers:
        return fail("; ".join(blockers))

    sanitized_contract = sanitize(contract)
    sanitized_receipt = sanitize(receipt)
    generated_at = dt.datetime.now(dt.timezone.utc).isoformat()
    page = render_html(sanitized_contract, sanitized_receipt, generated_at)
    blockers = scan_for_blockers(page)
    if blockers:
        return fail("rendered page contains blocked content: " + "; ".join(blockers))

    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(page)
    (out_dir / "receipt.json").write_text(json.dumps(sanitized_receipt, indent=2, ensure_ascii=False))
    (out_dir / "contract.redacted.json").write_text(json.dumps(sanitized_contract, indent=2, ensure_ascii=False))
    (out_dir / "README.txt").write_text(
        "Metaharness IO bundle. Review index.html first. Repository permissions control access.\n"
    )
    print(f"IO RENDER PASS: {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
