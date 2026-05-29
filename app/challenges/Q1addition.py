'''!SIX:
description = "Add two numbers"
difficulty = "easy"
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
!SIX.'''
a = int(input())
b = int(input())
print(a + b)
