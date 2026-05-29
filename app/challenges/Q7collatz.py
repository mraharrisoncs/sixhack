number = int(input())
steps = 0
sequence = []
sequence.append(number)
while number != 1:
    if number % 2 == 0:
        number = number / 2
        number = int(number)
    else:
        number = 3 * number + 1
    sequence.append(number)
    steps = steps + 1
total_steps = len(sequence) - 1
print(total_steps)

'''!SIX:
description = "Count steps in the Collatz sequence to reach 1"
difficulty = "medium"
topic = "iteration"
spec_level = "gcse"
hints = ["The sequence list is built but never used — why store every value if you only need the count?", "Integer division // avoids the need to cast back to int"]

[[test_cases]]
number = 1
name = "Normal"
inputs = [6]
expected_output = "8\n"

[[test_cases]]
number = 2
name = "Boundary - minimum input"
inputs = [1]
expected_output = "0\n"

[[test_cases]]
number = 3
name = "Normal - power of 2"
inputs = [8]
expected_output = "3\n"

[[test_cases]]
number = 4
name = "Normal - large with many steps"
inputs = [27]
expected_output = "111\n"

[[solutions]]
label = "Clean"
code = """
number = int(input())
steps = 0
while number != 1:
    number = number // 2 if number % 2 == 0 else 3 * number + 1
    steps += 1
print(steps)
"""

[[solutions]]
label = "Structured"
code = """
def collatz_steps(n):
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps

print(collatz_steps(int(input())))
"""
!SIX.'''
