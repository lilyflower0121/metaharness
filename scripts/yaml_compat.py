"""Tiny YAML compatibility helper for metaharness fixtures.

Uses PyYAML when available. Falls back to a deliberately small parser that
supports the subset used by metaharness contracts and skill frontmatter:
indentation-based mappings, lists of scalars, lists of one-level mappings,
strings, booleans, null, and inline [] lists.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

try:  # pragma: no cover - depends on environment
    import yaml as _pyyaml
except Exception:  # pragma: no cover
    _pyyaml = None


def load_text(text: str) -> Any:
    if _pyyaml is not None:
        return _pyyaml.safe_load(text)
    return _fallback_load(text)


def load_path(path: str | Path) -> Any:
    return load_text(Path(path).read_text(encoding="utf-8"))


def _strip_comment(line: str) -> str:
    in_quote = False
    quote = ""
    out = []
    for ch in line:
        if ch in {'"', "'"}:
            if not in_quote:
                in_quote = True; quote = ch
            elif quote == ch:
                in_quote = False; quote = ""
        if ch == "#" and not in_quote:
            break
        out.append(ch)
    return "".join(out).rstrip()


def _scalar(s: str) -> Any:
    s = s.strip()
    if s == "":
        return ""
    if s in {"[]", "[ ]"}:
        return []
    if s in {"{}", "{ }"}:
        return {}
    if s.lower() in {"null", "~"}:
        return None
    if s.lower() == "true":
        return True
    if s.lower() == "false":
        return False
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        if not inner:
            return []
        return [_scalar(x.strip()) for x in inner.split(",")]
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    return s


def _fallback_load(text: str) -> Any:
    lines = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        clean = _strip_comment(raw)
        if clean.strip():
            lines.append((len(clean) - len(clean.lstrip(" ")), clean.strip()))
    if not lines:
        return None

    root: Any = {}
    stack: list[tuple[int, Any]] = [(-1, root)]

    def parent_for(indent: int) -> Any:
        while stack and stack[-1][0] >= indent:
            stack.pop()
        return stack[-1][1]

    i = 0
    while i < len(lines):
        indent, content = lines[i]
        parent = parent_for(indent)
        if content.startswith("- "):
            if not isinstance(parent, list):
                raise ValueError(f"list item without list parent at: {content}")
            item = content[2:].strip()
            if ":" in item and not item.startswith(('"', "'")):
                k, v = item.split(":", 1)
                obj: dict[str, Any] = {k.strip(): _scalar(v.strip()) if v.strip() else {}}
                parent.append(obj)
                stack.append((indent, obj))
            else:
                parent.append(_scalar(item))
            i += 1
            continue
        if ":" not in content:
            raise ValueError(f"expected key: value at: {content}")
        key, val = content.split(":", 1)
        key = key.strip(); val = val.strip()
        if not isinstance(parent, dict):
            raise ValueError(f"mapping entry under non-mapping at: {content}")
        if val:
            parent[key] = _scalar(val)
        else:
            # decide container by next line
            next_is_list = i + 1 < len(lines) and lines[i + 1][0] > indent and lines[i + 1][1].startswith("- ")
            parent[key] = [] if next_is_list else {}
            stack.append((indent, parent[key]))
        i += 1
    return root
