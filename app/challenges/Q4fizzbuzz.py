'''!SIX:
description = "Print FizzBuzz from 1 to N"
difficulty = "medium"

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
!SIX.'''
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
