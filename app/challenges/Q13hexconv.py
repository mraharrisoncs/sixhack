n = int(input())
digits = "0123456789ABCDEF"
result = ""
while n > 0:
    result = digits[n % 16] + result
    n = n // 16
print(result)

'''!SIX:
description = "Convert a decimal integer to hexadecimal"
instructions = "Input a non-negative decimal integer and print its hexadecimal representation (using uppercase A–F)."
difficulty = "easy"
topic = "data representation"
spec_level = "gcse"
hints = ["Debug: Run with input 0 — same structural flaw as the binary converter. It should print 0 but the loop never runs.", "Structure: Fix the edge case for 0, then wrap it in def to_hex(n):."]

[[test_cases]]
number = 1
name = "Normal"
inputs = [255]
expected_output = "FF\n"

[[test_cases]]
number = 2
name = "Boundary - zero"
inputs = [0]
expected_output = "0\n"

[[test_cases]]
number = 3
name = "Normal - single hex digit"
inputs = [10]
expected_output = "A\n"

[[test_cases]]
number = 4
name = "Normal - 256"
inputs = [256]
expected_output = "100\n"

[[test_cases]]
number = 5
name = "Normal - 4096"
inputs = [4096]
expected_output = "1000\n"

[[solutions]]
label = "Clean"
code = """
decimal = int(input())
if decimal == 0:
    print("0")
else:
    digits = "0123456789ABCDEF"
    result = ""
    while decimal > 0:
        result = digits[decimal % 16] + result
        decimal //= 16
    print(result)
"""

[[solutions]]
label = "Minimal"
code = """
print(hex(int(input()))[2:].upper())
"""
!SIX.'''
