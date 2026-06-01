degrees = float(input())
step1 = degrees * 9
step2 = step1 / 5
step3 = step2 + 32
answer = step3
answer = round(answer, 1)
print(answer)

'''!SIX:
description = "Convert Celsius to Fahrenheit"
instructions = "Input a temperature in Celsius and output the equivalent in Fahrenheit, rounded to 1 decimal place."
difficulty = "easy"
topic = "arithmetic"
spec_level = "gcse"
hints = ["Debug: Test with 100 — you should get 212.0. Now check 0 and -40.", "Structure: Put the formula in def celsius_to_fahrenheit(degrees): returning the result — main block handles input and print only."]
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

[[solutions]]
label = "Clean"
code = """
celsius = float(input())
print(round(celsius * 9 / 5 + 32, 1))
"""

[[solutions]]
label = "Minimal"
code = """
print(round(float(input())*9/5+32,1))
"""
!SIX.'''
