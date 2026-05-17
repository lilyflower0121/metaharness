#!/usr/bin/env python3
"""Validate metaharness skill frontmatter and executable support-file presence."""
from __future__ import annotations
from pathlib import Path
import re, sys, yaml

def main() -> int:
    root=Path(__file__).resolve().parents[3]
    errors=[]
    for p in sorted((root/'skills').glob('*/SKILL.md')):
        text=p.read_text(encoding='utf-8')
        if not text.startswith('---'):
            errors.append(f'{p}: missing frontmatter')
            continue
        m=re.search(r'\n---\s*\n', text[3:])
        if not m:
            errors.append(f'{p}: unclosed frontmatter')
            continue
        fm=yaml.safe_load(text[3:m.start()+3])
        if not isinstance(fm, dict) or not fm.get('name') or not fm.get('description'):
            errors.append(f'{p}: missing name/description')
        if len(fm.get('description',''))>1024:
            errors.append(f'{p}: description too long')
        if not (p.parent/'references').exists():
            errors.append(f'{p}: missing references directory')
        if not (p.parent/'scripts').exists():
            errors.append(f'{p}: missing scripts directory')
    if errors:
        print('SKILL CONTRACT CHECK FAIL')
        for e in errors: print('-', e)
        return 1
    print('SKILL CONTRACT CHECK PASS')
    return 0
if __name__=='__main__':
    raise SystemExit(main())
