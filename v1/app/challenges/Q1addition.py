'''!SIX:
description = "Add two numbers"
difficulty = "easy"
max_lines = 1

[[test_cases]]
number = 1
name = "normal"
inputs = [1, 2]
expected_output = "3\n"

[[test_cases]]
number = 2
name = "boundary"
inputs = [0, 0]
expected_output = "0\n"

[[test_cases]]
number = 3
name = "extreme"
inputs = [1000000, 2000000]
expected_output = "3000000\n"
!SIX.'''
a = int(input())
b = int(input())
print(a + b)
