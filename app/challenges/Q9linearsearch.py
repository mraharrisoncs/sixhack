l = input().split(",")
t = input()
f = -1
x = 0
while x < len(l):
    if l[x] == t:
        f = x
    x = x + 1
print(f)

'''!SIX:
description = "Linear search: find the index of a target in a list"
instructions = "Input a comma-separated list of items and a target value, then print the index of the first occurrence of the target, or -1 if it is not found."
difficulty = "easy"
topic = "searching"
spec_level = "gcse"
hints = ["Debug: Try list=a,b,c,b and target=b — does it return 1 (first match) or 3 (last match)? Which is correct?", "Structure: Add break once found, put the logic in def linear_search(items, target):, and return -1 explicitly when not found."]

[[test_cases]]
number = 1
name = "Normal - item found"
inputs = ["3,1,4,1,5,9,2,6", "5"]
expected_output = "4\n"

[[test_cases]]
number = 2
name = "Normal - item not found"
inputs = ["3,1,4,1,5,9,2,6", "7"]
expected_output = "-1\n"

[[test_cases]]
number = 3
name = "Boundary - first element"
inputs = ["3,1,4,1,5", "3"]
expected_output = "0\n"

[[test_cases]]
number = 4
name = "Boundary - last element"
inputs = ["3,1,4,1,5", "5"]
expected_output = "4\n"

[[test_cases]]
number = 5
name = "Normal - duplicate values returns first"
inputs = ["3,1,4,1,5", "1"]
expected_output = "1\n"

[[solutions]]
label = "Clean"
code = """
items = input().split(",")
target = input()
for index, value in enumerate(items):
    if value == target:
        print(index)
        break
else:
    print(-1)
"""

[[solutions]]
label = "Structured"
code = """
def linear_search(items, target):
    for index, value in enumerate(items):
        if value == target:
            return index
    return -1

items = input().split(",")
target = input()
print(linear_search(items, target))
"""
!SIX.'''
