p = input()
score = 0
if len(p) >= 8:
    score = score + 1
if any(c.isupper() for c in p):
    score = score + 1
if any(c.isdigit() for c in p):
    score = score + 1
if score == 3:
    print("Strong")
if score == 2:
    print("Medium")
if score < 2:
    print("Weak")

'''!SIX:
description = "Rate password strength as Weak, Medium or Strong"
instructions = "Input a password string and rate its strength as Weak, Medium, or Strong based on its length, use of uppercase letters, digits, and special characters."
difficulty = "easy"
topic = "strings"
spec_level = "gcse"
hints = ["Debug: Test Password1 — the code gives Strong, but there is no special character check. Is that correct?", "Structure: Replace the three independent if statements with elif/else, add a special character check, then wrap scoring in def rate_password(password):."]

[[test_cases]]
number = 1
name = "Normal - strong password"
inputs = ["Hello123!"]
expected_output = "Strong\n"

[[test_cases]]
number = 2
name = "Normal - medium password"
inputs = ["hello123"]
expected_output = "Medium\n"

[[test_cases]]
number = 3
name = "Normal - weak password"
inputs = ["hello"]
expected_output = "Weak\n"

[[test_cases]]
number = 4
name = "Boundary - exactly 8 chars with upper and digit"
inputs = ["Abcdef1!"]
expected_output = "Strong\n"

[[test_cases]]
number = 5
name = "Boundary - 7 chars with upper and digit"
inputs = ["Abcde1!"]
expected_output = "Medium\n"

[[solutions]]
label = "Clean"
code = """
SPECIAL_CHARS = "!@#$%^&*"
password = input()
score = 0
if len(password) >= 8:
    score += 1
if any(c.isupper() for c in password):
    score += 1
if any(c.isdigit() for c in password):
    score += 1
if any(c in SPECIAL_CHARS for c in password):
    score += 1
if score >= 4:
    print("Strong")
elif score >= 2:
    print("Medium")
else:
    print("Weak")
"""

[[solutions]]
label = "Structured"
code = """
SPECIAL_CHARS = "!@#$%^&*"

def check_strength(password):
    rules = [
        len(password) >= 8,
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(c in SPECIAL_CHARS for c in password),
    ]
    score = sum(rules)
    if score >= 4:
        return "Strong"
    elif score >= 2:
        return "Medium"
    return "Weak"

print(check_strength(input()))
"""
!SIX.'''
