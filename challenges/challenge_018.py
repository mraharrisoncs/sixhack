"""
[challenge]
id = "challenge_018"
title = "Array Sum"
description = "Find the sum of all elements in a list"
difficulty = "beginner"
spec_level = "gcse"
topic = "Arrays"
free = true

instructions = '''
Read a comma-separated list of integers on one line and print their sum.
If the input is blank (empty list), print 0.

Examples:
  Input: 1,2,3
  Output: 6

  Input: 10,-5,3
  Output: 8

  Input: (blank line)
  Output: 0
'''

starter_code = '''
line = input().strip()
numbers = list(map(int, line.split(","))) if line else []
# Your code here: calculate and print the sum of numbers
'''

[[paradigms]]
paradigm = "all"
hints = [
    "Try input 1,2,3 — does your loop accumulate correctly? Start total at 0.",
]

[[paradigms.tests]]
name = "Basic positive list"
inputs = ["1,2,3"]
expected_output = "6"

[[paradigms.tests]]
name = "Mixed positive and negative"
inputs = ["10,-5,3"]
expected_output = "8"

[[paradigms.tests]]
name = "Empty list"
inputs = [""]
expected_output = "0"

[[paradigms.tests]]
name = "Single element"
inputs = ["5"]
expected_output = "5"

[[paradigms]]
paradigm = "structured"
hints = [
    "Write a sum_list(numbers) function that loops and accumulates, then call it.",
]
code = '''
def sum_list(numbers):
    total = 0
    for n in numbers:
        total += n
    return total

line = input().strip()
numbers = list(map(int, line.split(","))) if line else []
print(sum_list(numbers))
'''

[[paradigms]]
paradigm = "readable"
hints = [
    "Use a variable named running_total and update it clearly with each element.",
]
code = '''
# Read and sum a list of integers
line = input().strip()
numbers = list(map(int, line.split(","))) if line else []

running_total = 0
for number in numbers:
    running_total = running_total + number

print(running_total)
'''

[[paradigms]]
paradigm = "robust"
hints = [
    "Handle the empty input case — if the line is blank, numbers should be [] and the sum should be 0.",
]
code = '''
def sum_list(numbers):
    if not isinstance(numbers, list):
        raise TypeError("Expected a list")
    total = 0
    for item in numbers:
        if not isinstance(item, (int, float)):
            raise ValueError(f"Non-numeric value: {item}")
        total += item
    return total

try:
    line = input().strip()
    numbers = list(map(int, line.split(","))) if line else []
    print(sum_list(numbers))
except ValueError as e:
    print(f"Error: {e}")
'''

[[paradigms.tests]]
name = "Contains zero"
inputs = ["1,0,2"]
expected_output = "3"

[[paradigms]]
paradigm = "oop"
hints = [
    "Create a Summator class with an add(n) method and a total() method returning the accumulated sum.",
]
code = '''
class Summator:
    def __init__(self):
        self._total = 0

    def add(self, n):
        self._total += n

    def total(self):
        return self._total

line = input().strip()
numbers = list(map(int, line.split(","))) if line else []
summator = Summator()
for n in numbers:
    summator.add(n)
print(summator.total())
'''

[[paradigms]]
paradigm = "recursive"
hints = [
    "Return numbers[0] + sum_list(numbers[1:]) with base case: empty list returns 0.",
]
code = '''
def sum_list(numbers):
    if not numbers:
        return 0
    return numbers[0] + sum_list(numbers[1:])

line = input().strip()
numbers = list(map(int, line.split(","))) if line else []
print(sum_list(numbers))
'''

[[paradigms]]
paradigm = "minimalist"
hints = [
    "Python's built-in sum() does exactly this in one call.",
]
code = '''
line = input().strip()
print(sum(map(int, line.split(","))) if line else 0)
'''

"""

# Illustrative only
line = input().strip()
numbers = list(map(int, line.split(","))) if line else []
print(sum(numbers))
