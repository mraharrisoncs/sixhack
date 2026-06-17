"""
[challenge]
id = "challenge_003"
title = "Grade Calculator"
description = "Convert a percentage mark to a letter grade"
difficulty = "beginner"
spec_level = "gcse"
topic = "Selection"
free = true

instructions = '''
Input a percentage mark (0-100) and output the letter grade:
  A = 70 and above
  B = 60 to 69
  C = 50 to 59
  D = 40 to 49
  F = below 40

Example:
  Input: 75  Output: A
  Input: 35  Output: F
'''

starter_code = '''
x = int(input())
if x >= 40:
    g = "D"
if x >= 50:
    g = "C"
if x >= 60:
    g = "B"
if x >= 70:
    g = "A"
if x < 40:
    g = "F"
print(g)
'''

[[paradigms]]
paradigm = "all"
hints = [
    "Trace through a mark of 75 — count how many if statements fire. Is that efficient?",
    "Every condition is checked independently, so a mark of 85 sets g to D, then C, then B, then A — only the last assignment wins.",
]

[[paradigms.tests]]
name = "Normal - A grade"
inputs = ["85"]
expected_output = "A"

[[paradigms.tests]]
name = "Boundary - upper B"
inputs = ["69"]
expected_output = "B"

[[paradigms.tests]]
name = "Normal - C grade"
inputs = ["51"]
expected_output = "C"

[[paradigms.tests]]
name = "Boundary - lower D"
inputs = ["40"]
expected_output = "D"

[[paradigms.tests]]
name = "Normal - F grade"
inputs = ["35"]
expected_output = "F"

[[paradigms.tests]]
name = "Boundary - lower A"
inputs = ["70"]
expected_output = "A"

[[paradigms]]
paradigm = "structured"
hints = [
    "Rewrite using if/elif/else so only one branch runs per mark, then wrap it in def get_grade(mark):.",
]
code = '''
def get_grade(mark):
    if mark >= 70:
        return "A"
    elif mark >= 60:
        return "B"
    elif mark >= 50:
        return "C"
    elif mark >= 40:
        return "D"
    return "F"

mark = int(input())
print(get_grade(mark))
'''

[[paradigms]]
paradigm = "readable"
hints = [
    "Name your variable mark not x, and use descriptive grade boundaries like GRADE_A = 70.",
]
code = '''
# Grade boundaries
GRADE_A = 70
GRADE_B = 60
GRADE_C = 50
GRADE_D = 40

mark = int(input())

# Work from highest grade down so only one branch fires
if mark >= GRADE_A:
    grade = "A"
elif mark >= GRADE_B:
    grade = "B"
elif mark >= GRADE_C:
    grade = "C"
elif mark >= GRADE_D:
    grade = "D"
else:
    grade = "F"

print(grade)
'''

[[paradigms]]
paradigm = "robust"
hints = [
    "What if the mark is below 0 or above 100? Add a validation check before the grade logic.",
]
code = '''
def get_grade(mark):
    if not isinstance(mark, int):
        raise TypeError("Mark must be an integer")
    if mark < 0 or mark > 100:
        raise ValueError(f"Mark {mark} is out of range 0-100")
    if mark >= 70:
        return "A"
    elif mark >= 60:
        return "B"
    elif mark >= 50:
        return "C"
    elif mark >= 40:
        return "D"
    return "F"

try:
    mark = int(input())
    print(get_grade(mark))
except ValueError:
    print("Please enter a whole number between 0 and 100.")
'''

[[paradigms]]
paradigm = "oop"
hints = [
    "Create a GradeCalculator class with a grade(mark) method.",
]
code = '''
class GradeCalculator:
    BOUNDARIES = [(70, "A"), (60, "B"), (50, "C"), (40, "D"), (0, "F")]

    def __init__(self):
        self.last_grade = None

    def grade(self, mark):
        for boundary, letter in self.BOUNDARIES:
            if mark >= boundary:
                self.last_grade = letter
                return letter
        return "F"

calculator = GradeCalculator()
mark = int(input())
print(calculator.grade(mark))
'''

[[paradigms]]
paradigm = "recursive"
hints = [
    "Not a natural fit — but try defining grade(mark) that calls itself with mark-1 to reach boundaries.",
]
code = '''
BOUNDARIES = [(70, "A"), (60, "B"), (50, "C"), (40, "D"), (0, "F")]

def get_grade(mark, index=0):
    if index >= len(BOUNDARIES):
        return "F"
    boundary, letter = BOUNDARIES[index]
    if mark >= boundary:
        return letter
    return get_grade(mark, index + 1)

mark = int(input())
print(get_grade(mark))
'''

[[paradigms]]
paradigm = "minimalist"
hints = [
    "A chained ternary fits the whole grade table in one line.",
]
code = '''
m = int(input())
print("A" if m>=70 else "B" if m>=60 else "C" if m>=50 else "D" if m>=40 else "F")
'''

"""

# Illustrative only
x = int(input())
if x >= 40:
    g = "D"
if x >= 50:
    g = "C"
if x >= 60:
    g = "B"
if x >= 70:
    g = "A"
if x < 40:
    g = "F"
print(g)
