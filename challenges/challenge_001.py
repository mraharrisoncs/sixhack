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

hints = [
    "Debug: Run it with inputs 5 and 3 — does it print 8? Try 0 and 0, and a negative number.",
    "Structured: Wrap the addition in a function def add(a, b): that returns the result, then call it.",
    "Readable: Use descriptive names like first_number and second_number, and add a comment explaining the purpose.",
    "Robust: Validate that both inputs can be converted to integers — what happens if the user types a word?",
    "OOP: Create an Adder class with an add(a, b) method that returns the sum.",
    "Recursive: Think of addition as: add(a, b) = a + add(b-1, 1) with base case add(a, 0) = a.",
    "Minimalist: Can you do this in a single print statement without any variables?",
]

[[solutions]]
paradigm = "structured"
code = '''
def add(a, b):
    return a + b

first = int(input())
second = int(input())
print(add(first, second))
'''

[[solutions]]
paradigm = "readable"
code = '''
# Read two numbers and display their total
first_number = int(input())
second_number = int(input())
total = first_number + second_number
print(total)
'''

[[solutions]]
paradigm = "robust"
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

[[solutions]]
paradigm = "oop"
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

[[solutions]]
paradigm = "recursive"
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

[[solutions]]
paradigm = "minimalist"
code = '''
print(int(input()) + int(input()))
'''

[[tests]]
paradigm = "all"
name = "Normal"
inputs = ["5", "3"]
expected_output = "8"

[[tests]]
paradigm = "all"
name = "Boundary - both zero"
inputs = ["0", "0"]
expected_output = "0"

[[tests]]
paradigm = "all"
name = "Normal - large values"
inputs = ["1000000", "2000000"]
expected_output = "3000000"

[[tests]]
paradigm = "all"
name = "Normal - negative"
inputs = ["-4", "10"]
expected_output = "6"
"""

# Illustrative only
a = int(input())
b = int(input())
print(a + b)
