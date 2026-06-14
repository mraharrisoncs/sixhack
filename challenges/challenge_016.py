"""
[challenge]
id = "challenge_016"
title = "Password Checker"
description = "Rate password strength as Weak, Medium or Strong"
difficulty = "intermediate"
spec_level = "gcse"
topic = "Strings"
free = false

instructions = '''
Input a password string and rate its strength based on four criteria:
  1. Length of at least 8 characters
  2. Contains at least one uppercase letter
  3. Contains at least one digit
  4. Contains at least one special character (!@#$%^&*)

Score 1 point per criterion met:
  4 points = Strong
  2 or 3 points = Medium
  0 or 1 point = Weak

Examples:
  Input: Hello123!   Output: Strong
  Input: hello123    Output: Medium
  Input: hello       Output: Weak
'''

starter_code = '''
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
'''

hints = [
    "Debug: Test Password1 — the code gives Strong because score reaches 3, but it is missing the special character check.",
    "Debug: The thresholds are also wrong — 3 criteria met should not be Strong when there are 4 criteria in total.",
    "Structured: Add a special character check, fix the thresholds, and wrap scoring in def rate_password(password):.",
    "Readable: Use a list of named criteria functions and sum() over them for a clear, extensible design.",
    "Robust: Replace the three independent if statements with elif/else so only one strength label is printed.",
    "OOP: Create a PasswordStrengthChecker class with a rate(password) method and a criteria list.",
    "Recursive: Not a natural fit, but you could recursively check each rule in a list.",
    "Minimalist: sum() over a list of boolean expressions gives the score in one line.",
]

[[solutions]]
paradigm = "structured"
code = '''
SPECIAL_CHARS = "!@#$%^&*"

def score_password(password):
    rules = [
        len(password) >= 8,
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(c in SPECIAL_CHARS for c in password),
    ]
    return sum(rules)

def rate_password(password):
    score = score_password(password)
    if score >= 4:
        return "Strong"
    elif score >= 2:
        return "Medium"
    return "Weak"

print(rate_password(input()))
'''

[[solutions]]
paradigm = "readable"
code = '''
# Criteria for password strength
MINIMUM_LENGTH = 8
SPECIAL_CHARACTERS = "!@#$%^&*"

password = input()

# Check each strength criterion independently
has_minimum_length = len(password) >= MINIMUM_LENGTH
has_uppercase = any(character.isupper() for character in password)
has_digit = any(character.isdigit() for character in password)
has_special = any(character in SPECIAL_CHARACTERS for character in password)

# Count how many criteria are met
strength_score = sum([has_minimum_length, has_uppercase, has_digit, has_special])

# Classify based on total score
if strength_score >= 4:
    print("Strong")
elif strength_score >= 2:
    print("Medium")
else:
    print("Weak")
'''

[[solutions]]
paradigm = "robust"
code = '''
SPECIAL_CHARS = "!@#$%^&*"

def rate_password(password):
    if not isinstance(password, str):
        raise TypeError("Password must be a string")
    if not password:
        raise ValueError("Password cannot be empty")

    criteria = [
        len(password) >= 8,
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(c in SPECIAL_CHARS for c in password),
    ]
    score = sum(criteria)

    if score >= 4:
        return "Strong"
    elif score >= 2:
        return "Medium"
    return "Weak"

try:
    print(rate_password(input()))
except ValueError as e:
    print(f"Error: {e}")
'''

[[solutions]]
paradigm = "oop"
code = '''
class PasswordStrengthChecker:
    SPECIAL_CHARS = "!@#$%^&*"

    def __init__(self):
        self.criteria = [
            lambda p: len(p) >= 8,
            lambda p: any(c.isupper() for c in p),
            lambda p: any(c.isdigit() for c in p),
            lambda p: any(c in self.SPECIAL_CHARS for c in p),
        ]

    def rate(self, password):
        score = sum(check(password) for check in self.criteria)
        if score >= 4:
            return "Strong"
        elif score >= 2:
            return "Medium"
        return "Weak"

checker = PasswordStrengthChecker()
print(checker.rate(input()))
'''

[[solutions]]
paradigm = "recursive"
code = '''
SPECIAL_CHARS = "!@#$%^&*"
CRITERIA = [
    lambda p: len(p) >= 8,
    lambda p: any(c.isupper() for c in p),
    lambda p: any(c.isdigit() for c in p),
    lambda p: any(c in SPECIAL_CHARS for c in p),
]

def score(password, index=0):
    if index >= len(CRITERIA):
        return 0
    return int(CRITERIA[index](password)) + score(password, index + 1)

def rate_password(password):
    s = score(password)
    if s >= 4:
        return "Strong"
    elif s >= 2:
        return "Medium"
    return "Weak"

print(rate_password(input()))
'''

[[solutions]]
paradigm = "minimalist"
code = '''
SPECIAL = "!@#$%^&*"
p = input()
s = sum([len(p)>=8, any(c.isupper() for c in p), any(c.isdigit() for c in p), any(c in SPECIAL for c in p)])
print("Strong" if s>=4 else "Medium" if s>=2 else "Weak")
'''

[[tests]]
paradigm = "all"
name = "Normal - strong password"
inputs = ["Hello123!"]
expected_output = "Strong"

[[tests]]
paradigm = "all"
name = "Normal - medium password"
inputs = ["hello123"]
expected_output = "Medium"

[[tests]]
paradigm = "all"
name = "Normal - weak password"
inputs = ["hello"]
expected_output = "Weak"

[[tests]]
paradigm = "all"
name = "Boundary - exactly 8 chars with upper, digit, special"
inputs = ["Abcde1!x"]
expected_output = "Strong"

[[tests]]
paradigm = "all"
name = "Boundary - 7 chars with upper and digit only"
inputs = ["Abcde1!"]
expected_output = "Medium"
"""

# Illustrative only
SPECIAL_CHARS = "!@#$%^&*"
p = input()
score = 0
if len(p) >= 8:
    score += 1
if any(c.isupper() for c in p):
    score += 1
if any(c.isdigit() for c in p):
    score += 1
if any(c in SPECIAL_CHARS for c in p):
    score += 1
print("Strong" if score >= 4 else "Medium" if score >= 2 else "Weak")
