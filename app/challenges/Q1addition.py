a = int(input())
b = int(input())
print(a + b)

'''!SIX:
description = "Add two numbers"
instructions = "Input two numbers (one per line), add them together, and print the result."
difficulty = "easy"
topic = "arithmetic"
spec_level = "gcse"
hints = ["Debug: Run it with inputs 5 and 3 — does it print 8? Try 0 and 0, and a negative number.", "Structure: Wrap the addition in a function def add(a, b): that returns the result, then call it from the main block."]
max_lines = 1

[[test_cases]]
number = 1
name = "Normal"
inputs = [1, 2]
expected_output = "3\n"

[[test_cases]]
number = 2
name = "Boundary - both zero"
inputs = [0, 0]
expected_output = "0\n"

[[test_cases]]
number = 3
name = "Normal - large values"
inputs = [1000000, 2000000]
expected_output = "3000000\n"

[[solutions]]
label = "Minimal"
code = """
print(int(input()) + int(input()))
"""
!SIX.'''
