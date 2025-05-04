'''!SIX:
description: "A program to add two numbers."
test_cases:
  - number: 1
    name: "normal"
    inputs: [1, 2]
    expected_output: "3\n"
  - number: 2
    name: "boundary"
    inputs: [0, 0]
    expected_output: "30\n"
  - number: 3
    name: "extreme"
    inputs: [1000000, 2000000]
    expected_output: "3000000\n"
'''
a = int(input())
b = int(input())
print(a + b)