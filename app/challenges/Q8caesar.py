'''!SIX:
description = "Encode a lowercase message with a Caesar cipher"
difficulty = "medium"

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
!SIX.'''
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
