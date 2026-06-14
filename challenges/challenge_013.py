"""
[challenge]
id = "challenge_013"
title = "Decimal to Hexadecimal"
description = "Convert a decimal integer to hexadecimal"
difficulty = "beginner"
spec_level = "gcse"
topic = "Data Representation"
free = false

instructions = '''
Input a non-negative decimal integer and print its hexadecimal representation
using uppercase A-F.

Examples:
  Input: 255   Output: FF
  Input: 0     Output: 0
  Input: 10    Output: A
  Input: 256   Output: 100
'''

starter_code = '''
n = int(input())
digits = "0123456789ABCDEF"
result = ""
while n > 0:
    result = digits[n % 16] + result
    n = n // 16
print(result)
'''

hints = [
    "Debug: Run with input 0 — same structural flaw as the binary converter. It should print 0 but the loop never runs.",
    "Bug: The edge case for n=0 is missing — add an if check before the while loop.",
    "Structured: Fix the edge case for 0, then wrap it in def to_hex(n): returning a string.",
    "Readable: Name the digit lookup string HEX_DIGITS and use descriptive names like remainder, hex_string.",
    "Robust: What if the user enters a negative number? Add a validation check.",
    "OOP: Create a NumberConverter class with to_hex(n) and to_binary(n) methods.",
    "Recursive: to_hex(n) = to_hex(n//16) + HEX_DIGITS[n%16], base case n==0 returns ''.",
    "Minimalist: Python's hex() built-in does this — strip '0x' with [2:] and call .upper().",
]

[[solutions]]
paradigm = "structured"
code = '''
HEX_DIGITS = "0123456789ABCDEF"

def to_hex(n):
    if n == 0:
        return "0"
    result = ""
    while n > 0:
        result = HEX_DIGITS[n % 16] + result
        n //= 16
    return result

print(to_hex(int(input())))
'''

[[solutions]]
paradigm = "readable"
code = '''
# Convert decimal to hexadecimal using repeated division by 16
HEX_DIGITS = "0123456789ABCDEF"

decimal = int(input())

if decimal == 0:
    print("0")
else:
    hex_string = ""
    remaining = decimal
    while remaining > 0:
        # The remainder selects the hex digit: 10->A, 11->B, etc.
        remainder = remaining % 16
        hex_string = HEX_DIGITS[remainder] + hex_string
        remaining = remaining // 16
    print(hex_string)
'''

[[solutions]]
paradigm = "robust"
code = '''
HEX_DIGITS = "0123456789ABCDEF"

def to_hex(n):
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    if n < 0:
        raise ValueError("Input must be non-negative")
    if n == 0:
        return "0"
    result = ""
    while n > 0:
        result = HEX_DIGITS[n % 16] + result
        n //= 16
    return result

try:
    n = int(input())
    print(to_hex(n))
except ValueError as e:
    print(f"Error: {e}")
'''

[[solutions]]
paradigm = "oop"
code = '''
class NumberConverter:
    HEX_DIGITS = "0123456789ABCDEF"

    def __init__(self):
        self.last_result = None

    def to_hex(self, n):
        if n == 0:
            self.last_result = "0"
            return "0"
        result = ""
        while n > 0:
            result = self.HEX_DIGITS[n % 16] + result
            n //= 16
        self.last_result = result
        return result

converter = NumberConverter()
print(converter.to_hex(int(input())))
'''

[[solutions]]
paradigm = "recursive"
code = '''
HEX_DIGITS = "0123456789ABCDEF"

def to_hex(n):
    if n == 0:
        return ""
    return to_hex(n // 16) + HEX_DIGITS[n % 16]

n = int(input())
print(to_hex(n) or "0")
'''

[[solutions]]
paradigm = "minimalist"
code = '''
print(hex(int(input()))[2:].upper())
'''

[[tests]]
paradigm = "all"
name = "Normal"
inputs = ["255"]
expected_output = "FF"

[[tests]]
paradigm = "all"
name = "Boundary - zero"
inputs = ["0"]
expected_output = "0"

[[tests]]
paradigm = "all"
name = "Normal - single hex digit"
inputs = ["10"]
expected_output = "A"

[[tests]]
paradigm = "all"
name = "Normal - 256"
inputs = ["256"]
expected_output = "100"

[[tests]]
paradigm = "all"
name = "Normal - 4096"
inputs = ["4096"]
expected_output = "1000"
"""

# Illustrative only
n = int(input())
HEX_DIGITS = "0123456789ABCDEF"
if n == 0:
    print("0")
else:
    result = ""
    while n > 0:
        result = HEX_DIGITS[n % 16] + result
        n //= 16
    print(result)
