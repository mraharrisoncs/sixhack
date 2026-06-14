"""
[challenge]
id = "challenge_004"
title = "FizzBuzz"
description = "Print FizzBuzz from 1 to N"
difficulty = "beginner"
spec_level = "gcse"
topic = "Iteration"
free = true

instructions = '''
Input a number N and print the integers from 1 to N, replacing:
  - multiples of 3 with Fizz
  - multiples of 5 with Buzz
  - multiples of both 3 and 5 with FizzBuzz

Example (N=5):
  1
  2
  Fizz
  4
  Buzz
'''

starter_code = '''
n = int(input())
i = 1
while i <= n:
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    if i % 3 == 0 and i % 5 != 0:
        print("Fizz")
    if i % 5 == 0 and i % 3 != 0:
        print("Buzz")
    if i % 3 != 0 and i % 5 != 0:
        print(i)
    i = i + 1
'''

hints = [
    "Debug: Run it with n=15 — does every line come out correctly? Count how many conditions Python checks per number.",
    "Debug: Four independent if statements check overlapping conditions on every iteration — use elif/else to short-circuit.",
    "Structured: Use elif and else to short-circuit checks, then move the loop into def fizzbuzz(n):.",
    "Readable: Checking i % 15 == 0 for FizzBuzz is clearer than two separate modulo conditions combined with 'and'.",
    "Robust: What should happen for n=0 or a negative n? Add a guard at the top.",
    "OOP: Create a FizzBuzz class with a run(n) method that generates and prints the sequence.",
    "Recursive: Define fizzbuzz(i, n) that prints the value for i then calls fizzbuzz(i+1, n), with base case i > n.",
    "Minimalist: The whole thing can fit in a for loop with one print — use string multiplication with booleans.",
]

[[solutions]]
paradigm = "structured"
code = '''
def fizzbuzz_line(i):
    if i % 15 == 0:
        return "FizzBuzz"
    elif i % 3 == 0:
        return "Fizz"
    elif i % 5 == 0:
        return "Buzz"
    return str(i)

def fizzbuzz(n):
    for i in range(1, n + 1):
        print(fizzbuzz_line(i))

fizzbuzz(int(input()))
'''

[[solutions]]
paradigm = "readable"
code = '''
# Print FizzBuzz sequence from 1 to limit
limit = int(input())

for number in range(1, limit + 1):
    # Check divisibility in order: both, then each, then plain number
    is_fizz = number % 3 == 0
    is_buzz = number % 5 == 0

    if is_fizz and is_buzz:
        print("FizzBuzz")
    elif is_fizz:
        print("Fizz")
    elif is_buzz:
        print("Buzz")
    else:
        print(number)
'''

[[solutions]]
paradigm = "robust"
code = '''
def fizzbuzz(n):
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 1:
        raise ValueError("n must be at least 1")
    for i in range(1, n + 1):
        if i % 15 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)

try:
    n = int(input())
    fizzbuzz(n)
except ValueError as e:
    print(f"Error: {e}")
'''

[[solutions]]
paradigm = "oop"
code = '''
class FizzBuzz:
    def __init__(self):
        self.output = []

    def classify(self, i):
        if i % 15 == 0:
            return "FizzBuzz"
        elif i % 3 == 0:
            return "Fizz"
        elif i % 5 == 0:
            return "Buzz"
        return str(i)

    def run(self, n):
        self.output = [self.classify(i) for i in range(1, n + 1)]
        for line in self.output:
            print(line)

game = FizzBuzz()
game.run(int(input()))
'''

[[solutions]]
paradigm = "recursive"
code = '''
def fizzbuzz(i, n):
    if i > n:
        return
    if i % 15 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
    fizzbuzz(i + 1, n)

n = int(input())
fizzbuzz(1, n)
'''

[[solutions]]
paradigm = "minimalist"
code = '''
n = int(input())
for i in range(1, n+1):
    print("Fizz"*(i%3==0) + "Buzz"*(i%5==0) or i)
'''

[[tests]]
paradigm = "all"
name = "Normal - up to first FizzBuzz"
inputs = ["15"]
expected_output = "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz"

[[tests]]
paradigm = "all"
name = "Boundary - minimum input"
inputs = ["1"]
expected_output = "1"

[[tests]]
paradigm = "all"
name = "Boundary - first Fizz"
inputs = ["3"]
expected_output = "1\n2\nFizz"

[[tests]]
paradigm = "all"
name = "Boundary - first Buzz"
inputs = ["5"]
expected_output = "1\n2\nFizz\n4\nBuzz"
"""

# Illustrative only
n = int(input())
i = 1
while i <= n:
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    if i % 3 == 0 and i % 5 != 0:
        print("Fizz")
    if i % 5 == 0 and i % 3 != 0:
        print("Buzz")
    if i % 3 != 0 and i % 5 != 0:
        print(i)
    i = i + 1
