#!/usr/bin/env python3
"""
Migrate challenge files from flat hints/solutions/tests to [[paradigms]] structure.

Before:
    hints = ["Structured: ...", "Readable: ...", ...]
    [[solutions]]
    paradigm = "structured"
    code = '''...'''
    [[tests]]
    paradigm = "all"
    name = "..."

After:
    [[paradigms]]
    paradigm = "all"
    [[paradigms.tests]]
    name = "..."

    [[paradigms]]
    paradigm = "structured"
    hints = ["..."]
    code = '''...'''

Run from repo root:
    python scripts/migrate_paradigms.py [--dry-run]
"""
import re
import sys
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib


HINT_PREFIX_MAP = {
    'debug':      'all',
    'bug':        'all',
    'structured': 'structured',
    'readable':   'readable',
    'robust':     'robust',
    'oop':        'oop',
    'recursive':  'recursive',
    'minimalist': 'minimalist',
}

_PREFIX_RE = re.compile(
    r'^(' + '|'.join(HINT_PREFIX_MAP) + r'):\s*',
    re.IGNORECASE,
)


def classify_hint(text):
    """Return (paradigm, cleaned_text)."""
    m = _PREFIX_RE.match(text)
    if m:
        prefix = m.group(1).lower()
        return HINT_PREFIX_MAP[prefix], text[m.end():]
    return 'all', text


def escape_basic(s):
    """Escape a value for a TOML basic string (double-quoted)."""
    return (s
            .replace('\\', '\\\\')
            .replace('"',  '\\"')
            .replace('\n', '\\n')
            .replace('\r', '\\r')
            .replace('\t', '\\t'))


def toml_literal_ml(s):
    """Wrap s in TOML multi-line literal string (triple single-quotes)."""
    s = s.strip()
    if "'''" in s:
        # Fall back to escaped multi-line basic string
        return '"""\n' + s.replace('\\', '\\\\').replace('"', '\\"') + '\n"""'
    return f"'''\n{s}\n'''"


def toml_str(s):
    return '"' + escape_basic(s) + '"'


def toml_str_list(lst):
    items = ',\n    '.join(toml_str(s) for s in lst)
    return f'[\n    {items},\n]'


def build_toml(data):
    c    = data['challenge']
    solutions  = {s['paradigm']: s['code'] for s in data.get('solutions', [])}
    old_tests  = data.get('tests', [])
    old_hints  = c.pop('hints', [])

    # Classify hints by paradigm
    hints_by_paradigm: dict[str, list[str]] = {}
    for h in old_hints:
        paradigm, cleaned = classify_hint(h)
        hints_by_paradigm.setdefault(paradigm, []).append(cleaned)

    # Group tests by paradigm
    tests_by_paradigm: dict[str, list[dict]] = {}
    for t in old_tests:
        p = t.get('paradigm', 'all')
        tests_by_paradigm.setdefault(p, []).append(t)

    # Paradigm order: all first, then solution order
    paradigm_order = ['all'] + [s['paradigm'] for s in data.get('solutions', [])]

    lines = ['[challenge]']
    lines.append(f'id = {toml_str(c["id"])}')
    lines.append(f'title = {toml_str(c["title"])}')
    lines.append(f'description = {toml_str(c["description"])}')
    lines.append(f'difficulty = {toml_str(c["difficulty"])}')
    if c.get('spec_level'):
        lines.append(f'spec_level = {toml_str(c["spec_level"])}')
    if c.get('topic'):
        lines.append(f'topic = {toml_str(c["topic"])}')
    lines.append(f'free = {"true" if c.get("free") else "false"}')
    if c.get('max_lines'):
        lines.append(f'max_lines = {c["max_lines"]}')
    if c.get('max_bytes'):
        lines.append(f'max_bytes = {c["max_bytes"]}')
    lines.append('')
    lines.append(f'instructions = {toml_literal_ml(c["instructions"])}')
    lines.append('')
    lines.append(f'starter_code = {toml_literal_ml(c["starter_code"])}')
    lines.append('')

    for paradigm in paradigm_order:
        lines.append('[[paradigms]]')
        lines.append(f'paradigm = {toml_str(paradigm)}')

        if paradigm in hints_by_paradigm:
            lines.append(f'hints = {toml_str_list(hints_by_paradigm[paradigm])}')

        if paradigm in solutions:
            lines.append(f'code = {toml_literal_ml(solutions[paradigm])}')

        lines.append('')

        for t in tests_by_paradigm.get(paradigm, []):
            lines.append('[[paradigms.tests]]')
            lines.append(f'name = {toml_str(t["name"])}')
            inputs = [str(i) for i in t.get('inputs', [])]
            lines.append(f'inputs = [{", ".join(toml_str(i) for i in inputs)}]')
            lines.append(f'expected_output = {toml_str(t["expected_output"])}')
            lines.append('')

    return '\n'.join(lines)


def migrate_file(path: Path, dry_run=False):
    text = path.read_text(encoding='utf-8')
    m = re.search(r'^"""(.*?)"""', text, re.DOTALL)
    if not m:
        print(f'  SKIP {path.name} — no docstring')
        return

    try:
        data = tomllib.loads(m.group(1).strip())
    except Exception as e:
        print(f'  FAIL {path.name} — parse error: {e}')
        return

    if 'paradigms' in data:
        print(f'  SKIP {path.name} — already migrated')
        return

    new_toml = build_toml(data)

    # Verify the new TOML parses cleanly
    try:
        tomllib.loads(new_toml)
    except Exception as e:
        print(f'  FAIL {path.name} — generated TOML invalid: {e}')
        print('--- generated ---')
        print(new_toml)
        return

    new_docstring = f'"""\n{new_toml}\n"""'
    new_text = text[:m.start()] + new_docstring + text[m.end():]

    if dry_run:
        print(f'  DRY  {path.name}')
        print(new_toml[:500], '...' if len(new_toml) > 500 else '')
    else:
        path.write_text(new_text, encoding='utf-8')
        print(f'  OK   {path.name}')


def main():
    dry_run = '--dry-run' in sys.argv
    root = Path(__file__).parent.parent
    files = sorted(root.glob('challenges/challenge_*.py'))
    print(f'Migrating {len(files)} challenge files{"  [DRY RUN]" if dry_run else ""}...')
    for f in files:
        migrate_file(f, dry_run=dry_run)


if __name__ == '__main__':
    main()
