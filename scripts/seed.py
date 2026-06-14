#!/usr/bin/env python3
"""
Seed challenges from TOML docstrings in challenges/challenge_NNN.py

Run once before first deploy:
    python scripts/seed.py

To reseed from scratch, truncate the challenges table first:
    python scripts/seed.py --force

Safe to re-run without --force — skips if challenges already exist.
"""
import os
import re
import sys
from pathlib import Path

try:
    import tomllib           # Python 3.11+ stdlib
except ImportError:
    import tomli as tomllib  # pip install tomli for Python 3.10

sys.path.insert(0, str(Path(__file__).parent.parent))
from app import create_app, db
from app.models import Challenge


def extract_toml(py_path: Path) -> dict:
    """Extract and parse TOML from the module docstring of a .py file."""
    text = py_path.read_text(encoding='utf-8')
    m = re.search(r'^"""(.*?)"""', text, re.DOTALL)
    if not m:
        raise ValueError(f"No docstring found in {py_path.name}")
    return tomllib.loads(m.group(1).strip())


def seed(force=False):
    app = create_app()
    with app.app_context():
        existing = Challenge.query.count()
        if existing > 0 and not force:
            print(f"  {existing} challenges already in database — skipping seed.")
            print("  Run with --force to drop and reseed.")
            return

        if force and existing > 0:
            print(f"  --force: dropping {existing} existing challenges...")
            db.session.query(Challenge).delete()
            db.session.commit()

        files = sorted(Path(__file__).parent.parent.glob('challenges/challenge_*.py'))
        if not files:
            print("  No challenge files found in challenges/")
            return

        print(f"Seeding {len(files)} challenges...")
        for f in files:
            print(f"  {f.name} ...", end=' ', flush=True)
            try:
                data = extract_toml(f)
                c = data['challenge']
                db.session.add(Challenge(
                    id           = c['id'],
                    title        = c['title'],
                    description  = c['description'],
                    instructions = c['instructions'].strip(),
                    starter_code = c['starter_code'].strip(),
                    difficulty   = c['difficulty'],
                    spec_level   = c.get('spec_level'),
                    topic        = c.get('topic'),
                    free         = c['free'],
                    max_lines    = c.get('max_lines'),
                    max_bytes    = c.get('max_bytes'),
                    hints        = c.get('hints', []),
                    solutions    = data.get('solutions', []),
                    tests        = data.get('tests', []),
                ))
                print('OK')
            except Exception as e:
                print(f'FAILED — {e}')
                db.session.rollback()
                raise

        db.session.commit()
        print(f"\nSeeded {len(files)} challenges successfully.")


if __name__ == '__main__':
    force = '--force' in sys.argv
    seed(force=force)
