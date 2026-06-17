"""
[challenge]
id = "challenge_005"
title = "Celsius to Fahrenheit"
description = "Convert Celsius to Fahrenheit"
difficulty = "beginner"
spec_level = "gcse"
topic = "Arithmetic"
free = true
max_lines = 2

instructions = '''
Input a temperature in Celsius and output the equivalent in Fahrenheit,
rounded to 1 decimal place.

Formula: F = C * 9 / 5 + 32

Examples:
  Input: 100  Output: 212.0
  Input: 0    Output: 32.0
  Input: -40  Output: -40.0
'''

starter_code = '''
degrees = float(input())
step1 = degrees * 9
step2 = step1 / 5
step3 = step2 + 32
answer = step3
answer = round(answer, 1)
print(answer)
'''

[[paradigms]]
paradigm = "all"
hints = [
    "Test with 100 — you should get 212.0. Now check 0 and -40.",
    "The code is correct but uses 6 intermediate variables for a single formula — simplify.",
]

[[paradigms.tests]]
name = "Normal - boiling point"
inputs = ["100"]
expected_output = "212.0"

[[paradigms.tests]]
name = "Boundary - freezing point"
inputs = ["0"]
expected_output = "32.0"

[[paradigms.tests]]
name = "Normal - body temperature"
inputs = ["37"]
expected_output = "98.6"

[[paradigms.tests]]
name = "Boundary - equal in both scales"
inputs = ["-40"]
expected_output = "-40.0"

[[paradigms]]
paradigm = "structured"
hints = [
    "Put the formula in def celsius_to_fahrenheit(c): returning the result — main block handles input and print.",
]
code = '''
def celsius_to_fahrenheit(celsius):
    return round(celsius * 9 / 5 + 32, 1)

celsius = float(input())
print(celsius_to_fahrenheit(celsius))
'''

[[paradigms]]
paradigm = "readable"
hints = [
    "Use FAHRENHEIT_OFFSET = 32 and SCALE_FACTOR = 9/5 as named constants.",
]
code = '''
# Constants for the Celsius to Fahrenheit conversion
SCALE_FACTOR = 9 / 5
FREEZING_OFFSET = 32
DECIMAL_PLACES = 1

celsius = float(input())

# Apply the standard conversion formula
fahrenheit = celsius * SCALE_FACTOR + FREEZING_OFFSET
print(round(fahrenheit, DECIMAL_PLACES))
'''

[[paradigms]]
paradigm = "robust"
hints = [
    "What if the user types a non-numeric value? Wrap the conversion in a try/except.",
]
code = '''
def celsius_to_fahrenheit(celsius):
    if celsius < -273.15:
        raise ValueError("Temperature below absolute zero")
    return round(celsius * 9 / 5 + 32, 1)

try:
    celsius = float(input())
    print(celsius_to_fahrenheit(celsius))
except ValueError as e:
    print(f"Invalid input: {e}")
'''

[[paradigms]]
paradigm = "oop"
hints = [
    "Create a TemperatureConverter class with a to_fahrenheit(celsius) method.",
]
code = '''
class TemperatureConverter:
    def __init__(self):
        self.last_celsius = None
        self.last_fahrenheit = None

    def to_fahrenheit(self, celsius):
        self.last_celsius = celsius
        self.last_fahrenheit = round(celsius * 9 / 5 + 32, 1)
        return self.last_fahrenheit

converter = TemperatureConverter()
celsius = float(input())
print(converter.to_fahrenheit(celsius))
'''

[[paradigms]]
paradigm = "recursive"
hints = [
    "Not a natural fit, but you could compute C*9 by calling multiply(c, 9) recursively.",
]
code = '''
def multiply_by_nine_fifths(c, steps=9):
    if steps == 0:
        return 0
    return c / 5 + multiply_by_nine_fifths(c, steps - 1)

def celsius_to_fahrenheit(celsius):
    return round(multiply_by_nine_fifths(celsius) + 32, 1)

print(celsius_to_fahrenheit(float(input())))
'''

[[paradigms]]
paradigm = "minimalist"
hints = [
    "The formula fits on one line inside print() — no intermediate variables needed.",
]
code = '''
print(round(float(input())*9/5+32,1))
'''

"""

# Illustrative only
degrees = float(input())
step1 = degrees * 9
step2 = step1 / 5
step3 = step2 + 32
answer = round(step3, 1)
print(answer)
