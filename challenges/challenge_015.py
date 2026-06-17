"""
[challenge]
id = "challenge_015"
title = "Run-Length Encoder"
description = "Run-length encode a string (e.g. AAABBC -> 3A2B1C)"
difficulty = "intermediate"
spec_level = "a_level"
topic = "Algorithms"
free = false

instructions = '''
Input a string of uppercase letters and print its run-length encoding.
Each group of consecutive identical characters becomes a count followed
by the character.

Examples:
  Input: AAABBC   Output: 3A2B1C
  Input: A        Output: 1A
  Input: ABCD     Output: 1A1B1C1D
  Input: AAAAA    Output: 5A
'''

starter_code = '''
s = input()
o = ""
i = 0
while i < len(s):
    c = s[i]
    n = 1
    while i + n < len(s) and s[i + n] == c:
        n = n + 1
    o = o + str(n) + c
    i = i + n
print(o)
'''

[[paradigms]]
paradigm = "all"
hints = [
    "Test with AAABBC — you should get 3A2B1C. Try a single repeated character and a single unique character.",
    "This code is actually correct — the challenge is to find six cleaner ways to write it.",
]

[[paradigms.tests]]
name = "Normal - mixed runs"
inputs = ["AAABBC"]
expected_output = "3A2B1C"

[[paradigms.tests]]
name = "Boundary - single character"
inputs = ["A"]
expected_output = "1A"

[[paradigms.tests]]
name = "Normal - no repeats"
inputs = ["ABCD"]
expected_output = "1A1B1C1D"

[[paradigms.tests]]
name = "Normal - all same"
inputs = ["AAAAA"]
expected_output = "5A"

[[paradigms.tests]]
name = "Normal - two runs"
inputs = ["AABB"]
expected_output = "2A2B"

[[paradigms]]
paradigm = "structured"
hints = [
    "Extract a helper def count_run(s, start): that returns the run length at a position.",
]
code = '''
def count_run(data, start):
    char = data[start]
    count = 1
    while start + count < len(data) and data[start + count] == char:
        count += 1
    return char, count

def rle_encode(data):
    result = ""
    index = 0
    while index < len(data):
        char, count = count_run(data, index)
        result += str(count) + char
        index += count
    return result

print(rle_encode(input()))
'''

[[paradigms]]
paradigm = "readable"
hints = [
    "Use descriptive names like current_char, run_length, encoded instead of c, n, o.",
]
code = '''
# Run-length encoding: replace repeated characters with count + character
data = input()
encoded = ""
index = 0

while index < len(data):
    current_char = data[index]
    run_length = 1

    # Count how many times current_char repeats consecutively
    while index + run_length < len(data) and data[index + run_length] == current_char:
        run_length += 1

    encoded += str(run_length) + current_char
    index += run_length

print(encoded)
'''

[[paradigms]]
paradigm = "robust"
hints = [
    "What if the input contains lowercase letters, digits, or spaces? Add a validation check.",
]
code = '''
def rle_encode(data):
    if not isinstance(data, str):
        raise TypeError("Input must be a string")
    if not data:
        raise ValueError("Input cannot be empty")
    if not all(c.isupper() for c in data):
        raise ValueError("Input must contain only uppercase letters")

    result = ""
    index = 0
    while index < len(data):
        char = data[index]
        count = 1
        while index + count < len(data) and data[index + count] == char:
            count += 1
        result += str(count) + char
        index += count
    return result

try:
    print(rle_encode(input()))
except ValueError as e:
    print(f"Error: {e}")
'''

[[paradigms]]
paradigm = "oop"
hints = [
    "Create an RLEEncoder class with an encode(data) method and a decode(encoded) method.",
]
code = '''
class RLEEncoder:
    def __init__(self):
        self.last_encoded = None

    def encode(self, data):
        result = ""
        index = 0
        while index < len(data):
            char = data[index]
            count = 1
            while index + count < len(data) and data[index + count] == char:
                count += 1
            result += str(count) + char
            index += count
        self.last_encoded = result
        return result

    def decode(self, encoded):
        result = ""
        index = 0
        while index < len(encoded):
            count = int(encoded[index])
            char = encoded[index + 1]
            result += char * count
            index += 2
        return result

encoder = RLEEncoder()
print(encoder.encode(input()))
'''

[[paradigms]]
paradigm = "recursive"
hints = [
    "encode(s) = str(run_length) + s[0] + encode(s[run_length:]), base case empty string.",
]
code = '''
def count_run(data, index=0):
    if index >= len(data) or data[index] != data[0]:
        return index
    return count_run(data, index + 1)

def rle_encode(data):
    if not data:
        return ""
    run = count_run(data)
    return str(run) + data[0] + rle_encode(data[run:])

print(rle_encode(input()))
'''

[[paradigms]]
paradigm = "minimalist"
hints = [
    "Use itertools.groupby to group consecutive identical characters in one step.",
]
code = '''
from itertools import groupby
print("".join(str(len(list(g)))+k for k,g in groupby(input())))
'''

"""

# Illustrative only
s = input()
o = ""
i = 0
while i < len(s):
    c = s[i]
    n = 1
    while i + n < len(s) and s[i + n] == c:
        n = n + 1
    o = o + str(n) + c
    i = i + n
print(o)
