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

'''!SIX:
description = "Print FizzBuzz from 1 to N"
instructions = "Input a number N and print the integers from 1 to N, replacing multiples of 3 with Fizz, multiples of 5 with Buzz, and multiples of both with FizzBuzz."
difficulty = "medium"
topic = "iteration"
spec_level = "gcse"
hints = ["Debug: Run it with n=15 — does every line come out correctly? Count how many conditions Python checks per number.", "Structure: Use elif and else to short-circuit checks, then move the loop into a def fizzbuzz(n): function."]

[[test_cases]]
number = 1
name = "Normal - up to first FizzBuzz"
inputs = [15]
expected_output = "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz\n"

[[test_cases]]
number = 2
name = "Boundary - minimum input"
inputs = [1]
expected_output = "1\n"

[[test_cases]]
number = 3
name = "Boundary - first Fizz"
inputs = [3]
expected_output = "1\n2\nFizz\n"

[[test_cases]]
number = 4
name = "Boundary - first Buzz"
inputs = [5]
expected_output = "1\n2\nFizz\n4\nBuzz\n"

[[solutions]]
label = "Clean"
code = """
n = int(input())
for i in range(1, n + 1):
    if i % 15 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
"""

[[solutions]]
label = "Minimal"
code = """
n = int(input())
for i in range(1, n+1):
    print("Fizz"*(i%3==0) + "Buzz"*(i%5==0) or i)
"""
!SIX.'''
