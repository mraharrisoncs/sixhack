"""Utilities for parsing style feedback."""

import re


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
