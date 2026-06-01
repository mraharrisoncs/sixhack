n = int(input())
r = ""
while n > 0:
    r = str(n % 2) + r
    n = n // 2
print(r)

'''!SIX:
description = "Convert a decimal integer to binary"
instructions = "Input a non-negative decimal integer and print its binary representation as a string of 0s and 1s."
difficulty = "easy"
topic = "data representation"
spec_level = "gcse"
hints = ["Debug: Run with input 0 — what does it print? It should print 0, but the while loop never runs for zero.", "Structure: Fix the edge case for 0, then wrap the conversion in def to_binary(n): returning a string."]

[[test_cases]]
number = 1
name = "Normal"
inputs = [10]
expected_output = "1010\n"

[[test_cases]]
number = 2
name = "Boundary - zero"
inputs = [0]
expected_output = "0\n"

[[test_cases]]
number = 3
name = "Boundary - one"
inputs = [1]
expected_output = "1\n"

[[test_cases]]
number = 4
name = "Normal - power of two"
inputs = [8]
expected_output = "1000\n"

[[test_cases]]
number = 5
name = "Normal - 255"
inputs = [255]
expected_output = "11111111\n"

[[solutions]]
label = "Clean"
code = """
decimal = int(input())
if decimal == 0:
    print("0")
else:
    binary = ""
    while decimal > 0:
        binary = str(decimal % 2) + binary
        decimal //= 2
    print(binary)
"""

[[solutions]]
label = "Minimal"
code = """
print(bin(int(input()))[2:])
"""
!SIX.'''
