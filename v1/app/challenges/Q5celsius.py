'''!SIX:
description = "Convert Celsius to Fahrenheit"
difficulty = "easy"
max_lines = 2

[[test_cases]]
number = 1
name = "Normal - boiling point"
inputs = [100]
expected_output = "212.0\n"

[[test_cases]]
number = 2
name = "Boundary - freezing point"
inputs = [0]
expected_output = "32.0\n"

[[test_cases]]
number = 3
name = "Normal - body temperature"
inputs = [37]
expected_output = "98.6\n"

[[test_cases]]
number = 4
name = "Boundary - equal in both scales"
inputs = [-40]
expected_output = "-40.0\n"
!SIX.'''
degrees = float(input())
step1 = degrees * 9
step2 = step1 / 5
step3 = step2 + 32
answer = step3
answer = round(answer, 1)
print(answer)
