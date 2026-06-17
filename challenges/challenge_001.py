"""
[challenge]
id = "challenge_001"
title = "Add Two Numbers"
description = "Add two numbers entered one per line"
difficulty = "beginner"
spec_level = "gcse"
topic = "Arithmetic"
free = true

instructions = '''
Input two integers, one per line, and print their sum.

Example:
  Input: 5 then 3
  Output: 8
'''

starter_code = '''
a = int(input())
b = int(input())
print(a + b)
'''

[[paradigms]]
paradigm = "all"
hints = [
    "Run it with inputs 5 and 3 — does it print 8? Try 0 and 0, and a negative number.",
]

[[paradigms.tests]]
name = "Normal"
inputs = ["5", "3"]
expected_output = "8"

[[paradigms.tests]]
name = "Boundary - both zero"
inputs = ["0", "0"]
expected_output = "0"

[[paradigms.tests]]
name = "Normal - large values"
inputs = ["1000000", "2000000"]
expected_output = "3000000"

[[paradigms.tests]]
name = "Normal - negative"
inputs = ["-4", "10"]
expected_output = "6"

[[paradigms]]
paradigm = "structured"
hints = [
    "Wrap the addition in a function def add(a, b): that returns the result, then call it.",
]
code = '''
def add(a, b):
    return a + b

first = int(input())
second = int(input())
print(add(first, second))
'''

[[paradigms]]
paradigm = "readable"
hints = [
    "Use descriptive names like first_number and second_number, and add a comment explaining the purpose.",
]
code = '''
# Read two numbers and display their total
first_number = int(input())
second_number = int(input())
total = first_number + second_number
print(total)
'''

[[paradigms]]
paradigm = "robust"
hints = [
    "Validate that both inputs can be converted to integers — what happens if the user types a word?",
]
code = '''
def get_integer(prompt=""):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")

first = get_integer()
second = get_integer()
print(first + second)
'''

[[paradigms]]
paradigm = "oop"
hints = [
    "Create an Adder class with an add(a, b) method that returns the sum.",
]
code = '''
class Adder:
    def __init__(self):
        self.result = 0

    def add(self, a, b):
        self.result = a + b
        return self.result

adder = Adder()
first = int(input())
second = int(input())
print(adder.add(first, second))
'''

[[paradigms]]
paradigm = "recursive"
hints = [
    "Think of addition as: add(a, b) = a + add(b-1, 1) with base case add(a, 0) = a.",
]
code = '''
def add(a, b):
    if b == 0:
        return a
    if b > 0:
        return add(a + 1, b - 1)
    return add(a - 1, b + 1)

first = int(input())
second = int(input())
print(add(first, second))
'''

[[paradigms]]
paradigm = "minimalist"
hints = [
    "Can you do this in a single print statement without any variables?",
]
code = '''
print(int(input()) + int(input()))
'''

"""

# Illustrative only
a = int(input())
b = int(input())
print(a + b)
