"""Utilities for loading challenge files into the database and parsing style feedback."""

import os
import json
import re
import tomllib

from app.models import db, PythonProgram, TestCase


def parse_program_file(filepath):
    """
    Parse a challenge .py file, extracting embedded TOML metadata and the challenge code.
    Metadata is delimited by '''!SIX: ... !SIX.'''.
    Returns (metadata_dict, code_string).
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if "'''!SIX:" in content and "!SIX.'''" in content:
        metadata_start = content.find("'''!SIX:") + len("'''!SIX:")
        metadata_end = content.find("!SIX.'''", metadata_start)
        toml_content = content[metadata_start:metadata_end].strip()
        metadata = tomllib.loads(toml_content)
        code = content[metadata_end + len("!SIX.'''"):].strip()
    else:
        metadata = {}
        code = content.strip()

    return metadata, code


def populate_database():
    """
    Drop and recreate all tables, then load every challenge from the challenges directory.
    Called once on app startup.
    """
    db.drop_all()
    db.create_all()

    challenges_dir = os.path.join(os.path.dirname(__file__), 'challenges')
    for filename in sorted(os.listdir(challenges_dir)):
        if not filename.endswith('.py'):
            continue
        filepath = os.path.join(challenges_dir, filename)
        metadata, code = parse_program_file(filepath)

        program = PythonProgram(
            name=filename.replace('.py', ''),
            code=code,
            description=metadata.get('description'),
            difficulty=metadata.get('difficulty'),
            max_lines=metadata.get('max_lines'),
            max_bytes=metadata.get('max_bytes'),
        )
        db.session.add(program)
        db.session.commit()

        for tc in metadata.get('test_cases', []):
            db.session.add(TestCase(
                program_id=program.id,
                name=tc.get('name', 'Unnamed Test Case'),
                inputs=json.dumps(tc.get('inputs', [])),
                expected_output=tc.get('expected_output', '')
            ))
        db.session.commit()

    print("Database populated successfully.")


def extract_feedback(output, feedback_rules):
    """
    Match output (pylint stdout or AST result string) against a list of feedback rules.
    Each rule is a dict with keys: regex, message (None to use the matched text), delta.
    Returns (feedback_lines, total_score_delta).
    """
    feedback = []
    score_delta = 0
    for rule in feedback_rules:
        for match in re.findall(rule["regex"], output, re.MULTILINE):
            feedback.append(match if rule.get("message") is None else rule["message"])
            score_delta += rule.get("delta", 0)
    return feedback, score_delta
