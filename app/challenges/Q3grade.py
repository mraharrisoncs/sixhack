'''!SIX:
description = "Convert a percentage mark to a letter grade"
difficulty = "easy"

[[test_cases]]
number = 1
name = "Normal - A grade"
inputs = [85]
expected_output = "A\n"

[[test_cases]]
number = 2
name = "Boundary - upper B"
inputs = [69]
expected_output = "B\n"

[[test_cases]]
number = 3
name = "Normal - C grade"
inputs = [51]
expected_output = "C\n"

[[test_cases]]
number = 4
name = "Boundary - lower D"
inputs = [40]
expected_output = "D\n"

[[test_cases]]
number = 5
name = "Normal - F grade"
inputs = [35]
expected_output = "F\n"

[[test_cases]]
number = 6
name = "Boundary - lower A"
inputs = [70]
expected_output = "A\n"

[[test_cases]]
number = 7
name = "Boundary - upper F"
inputs = [39]
expected_output = "F\n"
!SIX.'''
# get the mark
x = int(input())
if x >= 40:
    g = "D"
if x >= 50:
    g = "C"
if x >= 60:
    g = "B"
if x >= 70:
    g = "A"
if x < 40:
    g = "F"
print(g)
