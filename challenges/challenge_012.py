"""
[challenge]
id = "challenge_012"
title = "Decimal to Binary"
description = "Convert a decimal integer to binary"
difficulty = "beginner"
spec_level = "gcse"
topic = "Data Representation"
free = true

instructions = '''
Input a non-negative decimal integer and print its binary representation
as a string of 0s and 1s.

Examples:
  Input: 10   Output: 1010
  Input: 0    Output: 0
  Input: 255  Output: 11111111
'''

starter_code = '''
n = int(input())
r = ""
while n > 0:
    r = str(n % 2) + r
    n = n // 2
print(r)
'''

[[paradigms]]
paradigm = "all"
hints = [
    "Run with input 0 — what does it print? It should print 0 but the while loop never runs for zero.",
    "The edge case for n=0 is missing — the loop body never executes and r stays empty.",
]

[[paradigms.tests]]
name = "Normal"
inputs = ["10"]
expected_output = "1010"

[[paradigms.tests]]
name = "Boundary - zero"
inputs = ["0"]
expected_output = "0"

[[paradigms.tests]]
name = "Boundary - one"
inputs = ["1"]
expected_output = "1"

[[paradigms.tests]]
name = "Normal - power of two"
inputs = ["8"]
expected_output = "1000"

[[paradigms.tests]]
name = "Normal - 255"
inputs = ["255"]
expected_output = "11111111"

[[paradigms]]
paradigm = "structured"
hints = [
    "Fix the edge case for 0, then wrap the conversion in def to_binary(n): returning a string.",
]
code = '''
def to_binary(n):
    if n == 0:
        return "0"
    binary = ""
    while n > 0:
        binary = str(n % 2) + binary
        n //= 2
    return binary

print(to_binary(int(input())))
'''

[[paradigms]]
paradigm = "readable"
hints = [
    "Name your accumulator binary_string and use descriptive comments explaining the repeated division.",
]
code = '''
# Convert decimal to binary using repeated division by 2
decimal = int(input())

if decimal == 0:
    print("0")
else:
    binary_string = ""
    remaining = decimal
    while remaining > 0:
        # The remainder when dividing by 2 gives the next binary digit
        remainder = remaining % 2
        binary_string = str(remainder) + binary_string
        remaining = remaining // 2
    print(binary_string)
'''

[[paradigms]]
paradigm = "robust"
hints = [
    "What if the user types a negative number? Add a check — negative binary representation is a separate topic.",
]
code = '''
def to_binary(n):
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    if n < 0:
        raise ValueError("Input must be non-negative")
    if n == 0:
        return "0"
    binary = ""
    while n > 0:
        binary = str(n % 2) + binary
        n //= 2
    return binary

try:
    n = int(input())
    print(to_binary(n))
except ValueError as e:
    print(f"Error: {e}")
'''

[[paradigms]]
paradigm = "oop"
hints = [
    "Create a NumberConverter class with a to_binary(n) method.",
]
code = '''
class NumberConverter:
    def __init__(self):
        self.last_result = None

    def to_binary(self, n):
        if n == 0:
            self.last_result = "0"
            return "0"
        binary = ""
        while n > 0:
            binary = str(n % 2) + binary
            n //= 2
        self.last_result = binary
        return binary

converter = NumberConverter()
print(converter.to_binary(int(input())))
'''

[[paradigms]]
paradigm = "recursive"
hints = [
    "to_binary(n) = to_binary(n//2) + str(n%2), base case n==0 returns '0' (or '' for recursion building up).",
]
code = '''
def to_binary(n):
    if n == 0:
        return "0"
    if n == 1:
        return "1"
    return to_binary(n // 2) + str(n % 2)

print(to_binary(int(input())))
'''

[[paradigms]]
paradigm = "minimalist"
hints = [
    "Python's bin() built-in does this — strip the '0b' prefix with [2:].",
]
code = '''
print(bin(int(input()))[2:])
'''

"""

# Illustrative only
n = int(input())
if n == 0:
    print("0")
else:
    r = ""
    while n > 0:
        r = str(n % 2) + r
        n //= 2
    print(r)
