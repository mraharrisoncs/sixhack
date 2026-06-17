"""
[challenge]
id = "challenge_007"
title = "Collatz Sequence"
description = "Count steps in the Collatz sequence to reach 1"
difficulty = "intermediate"
spec_level = "gcse"
topic = "Iteration"
free = true

instructions = '''
Input a positive integer and count how many steps the Collatz sequence takes to reach 1.

Rules:
  - If the number is even, halve it
  - If the number is odd, multiply by 3 and add 1
  - Count steps until you reach 1

Examples:
  Input: 6   Output: 8  (6->3->10->5->16->8->4->2->1)
  Input: 1   Output: 0
  Input: 8   Output: 3  (8->4->2->1)
'''

starter_code = '''
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
'''

[[paradigms]]
paradigm = "all"
hints = [
    "Try input 6 — the answer should be 8 steps. Does it output 8?",
    "The code maintains both a steps counter and a sequence list but only uses one of them — one is redundant.",
]

[[paradigms.tests]]
name = "Normal"
inputs = ["6"]
expected_output = "8"

[[paradigms.tests]]
name = "Boundary - minimum input"
inputs = ["1"]
expected_output = "0"

[[paradigms.tests]]
name = "Normal - power of 2"
inputs = ["8"]
expected_output = "3"

[[paradigms.tests]]
name = "Normal - large with many steps"
inputs = ["27"]
expected_output = "111"

[[paradigms]]
paradigm = "structured"
hints = [
    "Move the logic into def count_steps(n): — the sequence list is redundant if you only need the count.",
]
code = '''
def count_steps(n):
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps

print(count_steps(int(input())))
'''

[[paradigms]]
paradigm = "readable"
hints = [
    "Use integer division // instead of dividing then converting back to int with int().",
]
code = '''
# Count how many steps the Collatz sequence takes to reach 1
starting_number = int(input())
current_number = starting_number
step_count = 0

while current_number != 1:
    # Halve if even, otherwise apply 3n+1
    if current_number % 2 == 0:
        current_number = current_number // 2
    else:
        current_number = 3 * current_number + 1
    step_count += 1

print(step_count)
'''

[[paradigms]]
paradigm = "robust"
hints = [
    "What if the user enters 0 or a negative number? The Collatz sequence is only defined for positive integers.",
]
code = '''
def count_steps(n):
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    if n < 1:
        raise ValueError("Input must be a positive integer")
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps

try:
    n = int(input())
    print(count_steps(n))
except ValueError as e:
    print(f"Error: {e}")
'''

[[paradigms]]
paradigm = "oop"
hints = [
    "Create a CollatzSequence class with a count(n) method and a generate(n) method that returns the full sequence.",
]
code = '''
class CollatzSequence:
    def __init__(self):
        self.sequence = []

    def generate(self, n):
        self.sequence = [n]
        while n != 1:
            n = n // 2 if n % 2 == 0 else 3 * n + 1
            self.sequence.append(n)
        return self.sequence

    def count(self, n):
        return len(self.generate(n)) - 1

collatz = CollatzSequence()
print(collatz.count(int(input())))
'''

[[paradigms]]
paradigm = "recursive"
hints = [
    "count_steps(n) = 0 if n == 1, else 1 + count_steps(n//2 if n even else 3*n+1).",
]
code = '''
def count_steps(n):
    if n == 1:
        return 0
    if n % 2 == 0:
        return 1 + count_steps(n // 2)
    return 1 + count_steps(3 * n + 1)

print(count_steps(int(input())))
'''

[[paradigms]]
paradigm = "minimalist"
hints = [
    "A while loop with ternary selection fits in just a few lines.",
]
code = '''
n, s = int(input()), 0
while n != 1:
    n, s = (n//2 if n%2==0 else 3*n+1), s+1
print(s)
'''

"""

# Illustrative only
number = int(input())
steps = 0
while number != 1:
    number = number // 2 if number % 2 == 0 else 3 * number + 1
    steps += 1
print(steps)
