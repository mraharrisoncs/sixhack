# six(im).possible().things() — Claude Code Implementation Spec

---

## SCOPE

This spec covers four things:

1. **Database models** — replace `PythonProgram` and `TestCase` with `Challenge`, `Submission`, `User`, `Email`
2. **TOML challenge format** — 24 Python files with TOML docstrings as the authoring source
3. **Seed script** — parse TOML files and populate the database
4. **Input mode switching** — clicking the Debug stage tab sets interactive Skulpt input; clicking a unit test tab sets server-side execution (no visible toggle in the UI)

Everything else in the existing codebase (`run_code`, `test_code`, `CODE_STYLES`, `style_check`, pylint/AST checks, `renderFeedback`, autosave, hex score display, stage unlock logic) stays **unchanged**.

---

## 1. DATABASE MODELS

### File
`app/models.py` — replace the entire file.

Remove `PythonProgram` and `TestCase`. Add `Challenge`, `Submission`, `User`, `Email`.

```python
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(db.Model):
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80),  unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False, index=True)
    is_active     = db.Column(db.Boolean, default=True)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    submissions = db.relationship('Submission', backref='user', lazy=True,
                                  cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Challenge(db.Model):
    __tablename__ = 'challenges'

    id           = db.Column(db.String(20),  primary_key=True)   # e.g. 'challenge_001'
    title        = db.Column(db.String(200), nullable=False, index=True)
    description  = db.Column(db.Text, nullable=False)  # one-line summary → #instructions-goal
    instructions = db.Column(db.Text, nullable=False)  # full problem text → #instructions-body
    starter_code = db.Column(db.Text, nullable=False)  # blank stub shown in editor
    difficulty   = db.Column(db.String(20), nullable=False)  # 'beginner'|'intermediate'|'advanced'
    spec_level   = db.Column(db.String(20))                  # 'gcse'|'a_level'|None
    topic        = db.Column(db.String(100))                 # badge label
    free         = db.Column(db.Boolean, default=False, index=True)
    max_lines    = db.Column(db.Integer)   # minimalist constraint (nullable)
    max_bytes    = db.Column(db.Integer)   # minimalist constraint (nullable)

    # JSON columns
    solutions = db.Column(db.JSON, nullable=False)
    # [{paradigm: str, code: str}, ...] — model answers, not shown to students

    hints = db.Column(db.JSON, nullable=False)
    # [str, ...] — flat list of hint strings, shown in #hints-list

    tests = db.Column(db.JSON, nullable=False)
    # [{paradigm: str, name: str, inputs: [str,...], expected_output: str}, ...]
    # paradigm = "all" → runs for every style
    # paradigm = "structured" etc. → runs only for that style

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    submissions = db.relationship('Submission', backref='challenge', lazy=True,
                                  cascade='all, delete-orphan')


class Submission(db.Model):
    __tablename__ = 'submissions'

    id           = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.String(20), db.ForeignKey('challenges.id'),
                             nullable=False, index=True)
    paradigm     = db.Column(db.String(20), nullable=False)
    code         = db.Column(db.Text, nullable=False)
    score        = db.Column(db.Integer, default=0)

    test_results = db.Column(db.JSON)
    passed_tests = db.Column(db.Integer, default=0)
    total_tests  = db.Column(db.Integer, default=0)

    # Free tier — no account needed
    student_name  = db.Column(db.String(200))
    teacher_email = db.Column(db.String(120))

    # Pro tier — nullable for free tier
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Email(db.Model):
    __tablename__ = 'emails'

    id                  = db.Column(db.Integer, primary_key=True)
    submission_id       = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)
    to_email            = db.Column(db.String(120), nullable=False, index=True)
    student_name        = db.Column(db.String(200), nullable=False)
    status              = db.Column(db.String(20), default='pending')  # pending|sent|failed
    sendgrid_message_id = db.Column(db.String(255))
    error_message       = db.Column(db.Text)
    created_at          = db.Column(db.DateTime, default=datetime.utcnow)
    sent_at             = db.Column(db.DateTime)
```

---

## 2. FLASK ROUTES

### File
`app/sandbox/routes.py` — replace entirely.

The existing helper functions (`_run_pylint`, `_run_ast_check`, `_check_*`, `_combine_test_and_style_results`) are **unchanged** — copy them verbatim. Only the route handlers and model references change.

#### What changes
- All `PythonProgram.query` → `Challenge.query`
- All `TestCase` → removed (tests live in `Challenge.tests` JSON)
- Route URLs that used `<int:program_id>` → `<string:program_id>`
- `/sandbox/test_cases/<id>` now reads from `Challenge.tests` JSON, optionally filtered by `?style=`
- `/sandbox/load` returns `instructions` field (not `code`)
- `/sandbox/original_code/<id>` returns `starter_code` field

#### Full route file

```python
"""Route definitions for the six(im).possible().things() sandbox."""

import json
import os
import subprocess
import tempfile
import ast
import re
import sys

from flask import render_template, request, jsonify
from app.models import Challenge, Submission, db
from app.sandbox.runner import run_code, test_code
from app.utils import extract_feedback
from app.code_styles import CODE_STYLES


def setup_routes(app):

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    # ── /sandbox/programs ────────────────────────────────────────────────────
    # Consumed by loadPrograms() in scripts.js to build the level bar hexagons.
    # Returns all challenges ordered by id (challenge_001, challenge_002, ...).
    # Each object needs: id, name, description, difficulty, spec_level.
    # 'name' is used as the fallback label; 'description' is the tooltip/goal line.

    @app.route('/sandbox/programs', methods=['GET'])
    def get_programs():
        challenges = Challenge.query.order_by(Challenge.id).all()
        return jsonify([
            {
                "id": c.id,
                "name": c.title,
                "description": c.description,
                "difficulty": c.difficulty,
                "spec_level": c.spec_level,
                "topic": c.topic,
                "free": c.free,
            }
            for c in challenges
        ])

    # ── /sandbox/load ────────────────────────────────────────────────────────
    # Consumed by updateInstructions() in scripts.js.
    # Field names must match exactly what updateInstructions() reads:
    #   data.description  → #instructions-goal
    #   data.instructions → #instructions-body
    #   data.spec_level   → badge ('a_level' renders as 'A-Level', else 'GCSE')
    #   data.topic        → badge
    #   data.hints        → #hints-list (flat array of strings)
    #   data.max_lines    → stored as currentProgramMaxLines
    #   data.max_bytes    → stored as currentProgramMaxBytes

    @app.route('/sandbox/load', methods=['GET'])
    def load_program():
        program_id = request.args.get('program_id')
        c = Challenge.query.get(program_id)
        if not c:
            return jsonify({"error": "Challenge not found"}), 404
        return jsonify({
            "id": c.id,
            "name": c.title,
            "description": c.description,
            "instructions": c.instructions,
            "topic": c.topic,
            "spec_level": c.spec_level,
            "difficulty": c.difficulty,
            "hints": c.hints,           # already a Python list from JSON column
            "max_lines": c.max_lines,
            "max_bytes": c.max_bytes,
        })

    # ── /sandbox/original_code/<id> ──────────────────────────────────────────
    # Consumed by loadChallenge() in scripts.js.
    # Returns the blank starter stub shown in the editor.
    # NOT the model answer — that lives in Challenge.solutions and is never
    # sent to the student.

    @app.route('/sandbox/original_code/<string:program_id>', methods=['GET'])
    def get_original_code(program_id):
        c = Challenge.query.get(program_id)
        if not c:
            return jsonify({"error": "Challenge not found"}), 404
        return jsonify({"original_code": c.starter_code})

    # ── /sandbox/test_cases/<id> ─────────────────────────────────────────────
    # Consumed by loadTestCases() in scripts.js to build unit test tab buttons.
    # Tab label is built as: `▶ {index+1}: {test.name}`
    # Button click posts test.inputs to /sandbox/run and compares output to
    # test.expected_output with .trim().
    #
    # Optional ?style= query param filters to tests where paradigm == "all"
    # OR paradigm == the requested style. If omitted, returns all tests.

    @app.route('/sandbox/test_cases/<string:program_id>', methods=['GET'])
    def get_test_cases(program_id):
        c = Challenge.query.get(program_id)
        if not c:
            return jsonify({"error": "Challenge not found"}), 404

        style = request.args.get('style')
        tests = c.tests  # list from JSON column

        if style:
            tests = [t for t in tests if t.get('paradigm') in ('all', style)]

        return jsonify([
            {
                "name": t.get('name', f"Test {i+1}"),
                "inputs": t.get('inputs', []),
                "expected_output": t.get('expected_output', ''),
            }
            for i, t in enumerate(tests)
        ])

    # ── /sandbox/run ─────────────────────────────────────────────────────────
    # Unchanged — server-side execution for unit test tabs.
    # Request:  { code, input: [str, ...] }
    # Response: { output: str } | { error: str }

    @app.route('/sandbox/run', methods=['POST'])
    def run():
        try:
            data = request.json
            code = data.get('code', '')
            inputs = [str(i) for i in data.get('input', [])]
            return jsonify(run_code(code, inputs))
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # ── /sandbox/test ────────────────────────────────────────────────────────
    # Consumed by the All Tests button (Final stage).
    # Reads tests from Challenge.tests JSON, filtered to paradigm == "all" OR
    # paradigm == style_key. Passes to test_code() then _combine_test_and_style_results().

    @app.route('/sandbox/test', methods=['POST'])
    def run_tests():
        try:
            data = request.get_json()
            program_id = data.get('program_id')
            code = data.get('code')
            style_key = data.get('style')
            max_lines = data.get('max_lines')
            max_bytes = data.get('max_bytes')

            c = Challenge.query.get(program_id)
            if not c:
                return jsonify({"error": "Challenge not found"}), 404

            # Filter tests to those relevant for this style
            all_tests = c.tests or []
            relevant = [
                t for t in all_tests
                if t.get('paradigm') in ('all', style_key)
            ]

            test_cases = [
                {
                    "name": t.get('name', f"Test {i+1}"),
                    "inputs": t.get('inputs', []),
                    "expected_output": t.get('expected_output', ''),
                }
                for i, t in enumerate(relevant)
            ]

            results = test_code(code, test_cases)

            if style_key:
                final_score, combined_feedback, feedback_detail = _combine_test_and_style_results(
                    results, style_key, code,
                    max_lines=max_lines or c.max_lines,
                    max_bytes=max_bytes or c.max_bytes,
                )
            else:
                final_score = None
                combined_feedback = []
                feedback_detail = None

            return jsonify({
                "results": results,
                "score": final_score,
                "feedback": combined_feedback,
                "feedback_detail": feedback_detail,
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # ── /sandbox/styles ──────────────────────────────────────────────────────
    # Unchanged — returns CODE_STYLES for style tab construction.

    @app.route('/sandbox/styles', methods=['GET'])
    def get_code_styles():
        frontend_fields = ["key", "name", "description", "code_version"]
        return jsonify([{k: style[k] for k in frontend_fields} for style in CODE_STYLES])

    # ── /sandbox/style_check ─────────────────────────────────────────────────
    # Unchanged — called after every Debug run-button click.

    @app.route('/sandbox/style_check', methods=['POST'])
    def style_check():
        data = request.get_json()
        style_key = data.get('style')
        code = data.get('code')
        max_lines = data.get('max_lines')
        max_bytes = data.get('max_bytes')
        style = next((s for s in CODE_STYLES if s['key'] == style_key), None)
        if not style:
            return jsonify({"error": "Unknown style"}), 400

        results = {}
        base_score = 10

        if style.get('pylint_required'):
            pylint_output = _run_pylint(code, style.get('pylint_parameters'))
            feedback, score_delta = extract_feedback(pylint_output, style.get('pylint_feedback', []))
            results['pylint'] = {
                "score": max(0, min(10, base_score + score_delta)),
                "feedback": feedback or ["No major issues detected."]
            }

        if style.get('ast_required'):
            ast_result = _run_ast_check(style, code, max_lines, max_bytes)
            feedback, score_delta = extract_feedback(ast_result, style.get('ast_feedback', []))
            results['ast'] = {
                "score": max(0, min(10, base_score + score_delta)),
                "feedback": feedback or [ast_result or "AST checks passed."]
            }

        return jsonify(results)

    # ── Internal helpers ─────────────────────────────────────────────────────
    # All helper functions below are UNCHANGED from the original routes.py.
    # Copy them verbatim.

    def _run_pylint(code, pylint_args):
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.py', encoding='utf-8') as tmp:
            tmp.write(code)
            tmp_path = tmp.name
        try:
            cmd = [sys.executable, "-m", "pylint", tmp_path] + (pylint_args or [])
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            return result.stdout
        finally:
            os.unlink(tmp_path)

    def _run_ast_check(style, code, max_lines=None, max_bytes=None):
        check = style.get('ast_parameters', {}).get('check')
        dispatch = {
            "structured": lambda: _check_structured(code),
            "readable":   lambda: _check_readable(code),
            "robust":     lambda: _check_robust(code),
            "oop":        lambda: _check_oop(code),
            "recursive":  lambda: _check_recursive(code),
            "minimalist": lambda: _check_minimalist(code, max_lines=max_lines, max_bytes=max_bytes),
        }
        return dispatch[check]() if check in dispatch else ""

    # _check_structured, _check_readable, _check_robust, _check_oop,
    # _check_recursive, _check_minimalist, _combine_test_and_style_results
    # — copy all verbatim from the original routes.py
```

---

## 3. TOML CHALLENGE FORMAT

### Location
`challenges/challenge_NNN.py` — 24 files. Committed to git. Listed in `.railwayignore` so they are not deployed (the seeded database is the production source of truth).

### Rules
- The Python file's module docstring contains TOML. Python code below is illustrative only and is never executed by the app.
- `hints` is a **flat list of strings** — not per-paradigm objects. The frontend iterates `hints.forEach(hint => { li.textContent = hint })`.
- `tests[].inputs` is an array of strings — one string per `input()` call in the student's code.
- `tests[].expected_output` is a string matched against stdout with `.trim()`.
- `tests[].paradigm = "all"` runs for every style. A specific paradigm name runs only for that style.
- `starter_code` is the blank stub the student starts from — not the model answer.

### Example file — `challenges/challenge_001.py`

```python
"""
[challenge]
id = "challenge_001"
title = "Sum a List"
description = "Add up all the numbers in a list"
difficulty = "beginner"
spec_level = "gcse"
topic = "Lists"
free = true
max_lines = 1
max_bytes = 40

instructions = """
Write a function called solve(numbers) that returns the sum of all the numbers in a list.

Examples:
  solve([1, 2, 3]) returns 6
  solve([10, 20]) returns 30
  solve([]) returns 0

Your function will be called with a list already created — you do not need to use input().
"""

starter_code = """
def solve(numbers):
    # Your code here
    pass

# Test your function below
print(solve([1, 2, 3]))   # should print 6
"""

hints = [
    "Use a loop to go through each number, keeping a running total.",
    "Python has a built-in function that adds up a list — can you find it?",
    "What should you return when the list is empty?",
    "For recursive: what is the base case when the list has no items left?",
    "For OOP: what state does your class need to keep track of?",
    "For minimalist: can you do this in one line using a built-in function?"
]

[[solutions]]
paradigm = "structured"
code = """
def solve(numbers):
    total = 0
    for num in numbers:
        total = total + num
    return total
"""

[[solutions]]
paradigm = "readable"
code = """
def solve(numbers):
    running_total = 0
    for number in numbers:
        running_total += number
    return running_total
"""

[[solutions]]
paradigm = "robust"
code = """
def solve(numbers):
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list")
    if not all(isinstance(n, (int, float)) for n in numbers):
        raise TypeError("All elements must be numbers")
    total = 0
    for num in numbers:
        total += num
    return total
"""

[[solutions]]
paradigm = "oop"
code = """
class Accumulator:
    def __init__(self):
        self.total = 0

    def add(self, n):
        self.total += n

def solve(numbers):
    acc = Accumulator()
    for n in numbers:
        acc.add(n)
    return acc.total
"""

[[solutions]]
paradigm = "recursive"
code = """
def solve(numbers):
    if not numbers:
        return 0
    return numbers[0] + solve(numbers[1:])
"""

[[solutions]]
paradigm = "minimalist"
code = """
def solve(numbers): return sum(numbers)
"""

[[tests]]
paradigm = "all"
name = "Basic sum"
inputs = []
expected_output = "6"

[[tests]]
paradigm = "all"
name = "Larger values"
inputs = []
expected_output = "60"

[[tests]]
paradigm = "all"
name = "Empty list"
inputs = []
expected_output = "0"

[[tests]]
paradigm = "all"
name = "Single item"
inputs = []
expected_output = "5"

[[tests]]
paradigm = "robust"
name = "Non-list input raises TypeError"
inputs = []
expected_output = "TypeError"

[[tests]]
paradigm = "minimalist"
name = "One-liner check"
inputs = []
expected_output = "6"
"""

# Illustrative only — not executed by the app
def solve(numbers):
    return sum(numbers)

print(solve([1, 2, 3]))   # 6
```

### TOML field reference

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | string | ✓ | `"challenge_001"` through `"challenge_024"` |
| `title` | string | ✓ | Short title |
| `description` | string | ✓ | One line → `#instructions-goal` |
| `difficulty` | string | ✓ | `beginner` / `intermediate` / `advanced` |
| `spec_level` | string | | `gcse` / `a_level` — omit if neither |
| `topic` | string | | Badge label e.g. `"Lists"` |
| `free` | bool | ✓ | `true` for 001–012, `false` for 013–024 |
| `instructions` | string | ✓ | Full problem text → `#instructions-body` |
| `starter_code` | string | ✓ | Blank stub shown in editor |
| `max_lines` | int | | Minimalist line constraint |
| `max_bytes` | int | | Minimalist byte constraint |
| `hints` | array of strings | ✓ | Flat list → `#hints-list` |
| `solutions[].paradigm` | string | ✓ | One of the six paradigm keys |
| `solutions[].code` | string | ✓ | Model answer — not shown to students |
| `tests[].paradigm` | string | ✓ | `"all"` or a specific paradigm key |
| `tests[].name` | string | ✓ | Unit test tab label |
| `tests[].inputs` | array of strings | ✓ | One string per `input()` call |
| `tests[].expected_output` | string | ✓ | Matched against stdout with `.trim()` |

---

## 4. SEED SCRIPT

### File
`scripts/seed.py` — create this file.

```python
#!/usr/bin/env python3
"""
Seed challenges from TOML docstrings in challenges/challenge_NNN.py

Run once before first deploy:
    python scripts/seed.py

Safe to re-run — skips if challenges already exist.
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


def seed():
    app = create_app()
    with app.app_context():
        existing = Challenge.query.count()
        if existing > 0:
            print(f"⚠  {existing} challenges already in database — skipping seed.")
            return

        files = sorted(Path(__file__).parent.parent.glob('challenges/challenge_*.py'))
        if not files:
            print("❌  No challenge files found in challenges/")
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
                    instructions = c['instructions'],
                    starter_code = c['starter_code'],
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
                print('✓')
            except Exception as e:
                print(f'❌  {e}')
                db.session.rollback()
                raise

        db.session.commit()
        print(f"\n✅  Seeded {len(files)} challenges successfully.")


if __name__ == '__main__':
    seed()
```

---

## 5. JAVASCRIPT — INPUT MODE SWITCHING

### File
`static/js/scripts.js` — targeted additions only. Everything else unchanged.

### What needs adding

The existing `runWithSkulpt(code, headerMsg)` already handles interactive input perfectly — it renders an inline `<input>` element when the student's code calls `input()`. This is the Debug mode. **Do not modify it.**

Unit tests run server-side via `/sandbox/run`. **Do not modify that.**

What's needed: clicking the **Debug stage tab** (`#stage-debug`) configures Skulpt to use its existing interactive `inputfun`. Clicking any **unit test tab button** (inside `#tab-buttons`) marks that the current execution context is server-side (which it already is). No visible toggle in the UI — the switching is implicit in which panel is active.

The only concrete addition is ensuring `#stage-debug` click **also re-initialises** the Skulpt `inputfun` to the interactive version, in case it was ever reconfigured. And `#stage-unit` click does nothing extra — server-side runs don't touch Skulpt config.

### Addition 1 — module-level Skulpt input state

Add these at the top of `scripts.js`, alongside the existing module-level variables:

```javascript
// ── Skulpt input mode ─────────────────────────────────────────────────────
// 'interactive' = inline input element in output window (Debug stage)
// 'server'      = unit test tabs post to /sandbox/run, Skulpt not used
let skulptInputMode = 'interactive';
```

### Addition 2 — stage tab click handlers update input mode

The existing `switchStage(stage)` function is called by the three stage tab listeners already in `DOMContentLoaded`. Modify those listeners to also set `skulptInputMode`:

```javascript
// Find the existing listeners in DOMContentLoaded and replace them:

document.getElementById('stage-debug').addEventListener('click', () => {
    skulptInputMode = 'interactive';
    switchStage('debug');
});

document.getElementById('stage-unit').addEventListener('click', () => {
    skulptInputMode = 'server';
    switchStage('unit');
});

document.getElementById('stage-final').addEventListener('click', () => {
    if (!document.getElementById('stage-final').disabled) {
        skulptInputMode = 'server';
        switchStage('final');
    }
});
```

### Addition 3 — pass style to loadTestCases

The `/sandbox/test_cases/<id>` route now accepts an optional `?style=` query param so it only returns tests relevant to the active paradigm. Update the fetch call inside `loadTestCases(programId)`:

```javascript
// Find this line in loadTestCases():
fetch(`/sandbox/test_cases/${programId}`)

// Replace with:
fetch(`/sandbox/test_cases/${programId}?style=${currentTab}`)
```

### Nothing else changes

The `runWithSkulpt` function already passes its own `inputfun` closure to `Sk.configure` on every call — it self-configures. The `skulptInputMode` variable is informational state that documents what mode is active; `runWithSkulpt` doesn't need to read it because it's only ever called from the `#run-button` handler (Debug stage), which is always interactive.

---

## 6. FILES TO CREATE / MODIFY

```
app/
  models.py                  REPLACE — remove PythonProgram/TestCase, add Challenge/Submission/User/Email

app/sandbox/
  routes.py                  REPLACE — update model references, string IDs, tests from JSON

challenges/
  challenge_001.py           CREATE × 24
  challenge_002.py
  ...
  challenge_024.py

scripts/
  seed.py                    CREATE

static/js/scripts.js         MODIFY — add skulptInputMode variable, update 3 stage tab listeners,
                                       update loadTestCases fetch to include ?style=

.railwayignore               CREATE or MODIFY — add: challenges/
```

---

## 7. IMPLEMENTATION CHECKLIST

**Models**
- [ ] `app/models.py` created with `User`, `Challenge`, `Submission`, `Email`
- [ ] `Challenge.hints` is JSON array of strings (not objects)
- [ ] `Challenge.tests` is JSON array with `paradigm`, `name`, `inputs`, `expected_output`
- [ ] `Challenge.instructions` and `Challenge.starter_code` are separate fields
- [ ] `db.create_all()` or migration creates all four tables

**Routes**
- [ ] `/sandbox/programs` — returns `title` as `name`, ordered by `id`
- [ ] `/sandbox/load` — returns `instructions` field (not `code`), `hints` as flat string list
- [ ] `/sandbox/original_code/<id>` — returns `starter_code`, route uses `<string:program_id>`
- [ ] `/sandbox/test_cases/<id>` — reads from `Challenge.tests` JSON, filters by `?style=`
- [ ] `/sandbox/test` — filters tests by paradigm before passing to `test_code()`
- [ ] `/sandbox/run` — unchanged
- [ ] `/sandbox/styles` — unchanged
- [ ] `/sandbox/style_check` — unchanged
- [ ] All `_check_*` and `_combine_test_and_style_results` helpers — copied verbatim

**Challenges (24 files)**
- [ ] `challenges/challenge_001.py` through `challenge_024.py`
- [ ] 001–012: `free = true` | 013–024: `free = false`
- [ ] Each has `description` (one line), `instructions` (full text), `starter_code` (stub)
- [ ] Each has 6 paradigm `[[solutions]]` entries
- [ ] Each has flat `hints` string list
- [ ] Each has at least 4 `[[tests]]` entries covering base cases
- [ ] Quick parse check: `python -c "import tomllib; t=open('challenges/challenge_001.py').read(); tomllib.loads(t.split('\"\"\"')[1])"`

**Seed**
- [ ] `python scripts/seed.py` runs without errors
- [ ] 24 rows in `challenges` table
- [ ] Running seed.py twice → still 24 rows (idempotent)
- [ ] `Challenge.hints` stored as list (not JSON string)

**JavaScript**
- [ ] `skulptInputMode` variable added at module level
- [ ] Three stage tab listeners updated to set `skulptInputMode`
- [ ] `loadTestCases` fetch updated to pass `?style=${currentTab}`
- [ ] `runWithSkulpt` and `#run-button` handler — unchanged
- [ ] Unit test tab buttons — unchanged
- [ ] `#all-tests-button` handler — unchanged

**Deployment**
- [ ] `challenges/` added to `.railwayignore`
- [ ] Seed run locally before first Railway deploy

---

## 8. NOTES FOR CLAUDE CODE

1. **`_check_*` helpers and `_combine_test_and_style_results`** — copy all of these verbatim from the original `routes.py`. They are correct and must not be modified.

2. **`hints` shape** — must be a Python list of strings in the database. `updateInstructions()` does `hints.forEach(hint => { li.textContent = hint })`. If hints are stored as JSON string rather than parsed list, the route must call `json.loads()` before returning. With SQLAlchemy's `db.Column(db.JSON)`, this is handled automatically — no manual parsing needed.

3. **`starter_code` vs model answer** — `/sandbox/original_code/<id>` returns `Challenge.starter_code` (the blank stub). The `solutions` array contains model answers and is never sent to the frontend in MVP.

4. **String IDs in routes** — use `<string:program_id>` not `<int:program_id>`. The frontend sends `'challenge_001'` as the program ID everywhere.

5. **`skulptInputMode` is informational** — `runWithSkulpt` self-configures its `inputfun` on every call and doesn't read this variable. The variable exists to make the mode explicit for future features (e.g. a pre-populated Skulpt test runner in a later phase).

6. **TOML triple-quote nesting** — the outer `"""` is Python's docstring delimiter. Multiline strings inside the TOML use `"""` too, which works because the regex `re.search(r'^"""(.*?)"""', text, re.DOTALL)` matches the **first** opening and **first** closing triple-quote pair. Keep multiline TOML values on separate lines with no leading `"""` on the same line as the key to avoid edge cases.

7. **Python version** — use `import tomllib` (stdlib, Python 3.11+). Fallback: `pip install tomli` and `import tomli as tomllib`.

8. **Idempotent seed** — `seed.py` checks `Challenge.query.count() > 0` and exits early. To reseed from scratch, truncate the `challenges` table first.
