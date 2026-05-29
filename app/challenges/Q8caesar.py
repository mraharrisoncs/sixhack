msg = input()
s = int(input())
out = ""
i = 0
while i < len(msg):
    c = msg[i]
    n = ord(c)
    n = n - 97
    n = n + s
    n = n % 26
    n = n + 97
    out = out + chr(n)
    i = i + 1
print(out)

'''!SIX:
description = "Encode a lowercase message with a Caesar cipher"
difficulty = "medium"
topic = "strings"
spec_level = "gcse"
hints = ["Single-letter variable names make the logic hard to follow", "Python's for loop can iterate over characters directly — no index needed"]

[[test_cases]]
number = 1
name = "Normal"
inputs = ["hello", 3]
expected_output = "khoor\n"

[[test_cases]]
number = 2
name = "Boundary - wrap around z to a"
inputs = ["xyz", 3]
expected_output = "abc\n"

[[test_cases]]
number = 3
name = "Boundary - zero shift"
inputs = ["python", 0]
expected_output = "python\n"

[[test_cases]]
number = 4
name = "Normal - full alphabet"
inputs = ["abcdefghijklmnopqrstuvwxyz", 1]
expected_output = "bcdefghijklmnopqrstuvwxyza\n"

[[test_cases]]
number = 5
name = "Normal - ROT13"
inputs = ["hello", 13]
expected_output = "uryyb\n"

[[solutions]]
label = "Clean"
code = """
message = input()
shift = int(input())
result = ""
for char in message:
    shifted = (ord(char) - ord('a') + shift) % 26 + ord('a')
    result += chr(shifted)
print(result)
"""

[[solutions]]
label = "Minimal"
code = """
msg, shift = input(), int(input())
print("".join(chr((ord(c) - 97 + shift) % 26 + 97) for c in msg))
"""
!SIX.'''
