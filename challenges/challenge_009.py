"""
[challenge]
id = "challenge_009"
title = "Linear Search"
description = "Linear search: find the index of a target in a list"
difficulty = "beginner"
spec_level = "gcse"
topic = "Searching"
free = true

instructions = '''
Input a comma-separated list of items and a target value, then print the index
of the first occurrence of the target, or -1 if it is not found.

Examples:
  Input: 3,1,4,1,5,9  then 5   Output: 4
  Input: 3,1,4,1,5    then 7   Output: -1
  Input: 3,1,4,1,5    then 3   Output: 0
'''

starter_code = '''
l = input().split(",")
t = input()
f = -1
x = 0
while x < len(l):
    if l[x] == t:
        f = x
    x = x + 1
print(f)
'''

[[paradigms]]
paradigm = "all"
hints = [
    "Try list=a,b,c,b and target=b — does it return 1 (first match) or 3 (last match)? Which is correct?",
    "The code updates f on every match, so the last occurrence wins instead of the first.",
]

[[paradigms.tests]]
name = "Normal - item found"
inputs = ["3,1,4,1,5,9,2,6", "5"]
expected_output = "4"

[[paradigms.tests]]
name = "Normal - item not found"
inputs = ["3,1,4,1,5,9,2,6", "7"]
expected_output = "-1"

[[paradigms.tests]]
name = "Boundary - first element"
inputs = ["3,1,4,1,5", "3"]
expected_output = "0"

[[paradigms.tests]]
name = "Boundary - last element"
inputs = ["3,1,4,1,5", "5"]
expected_output = "4"

[[paradigms.tests]]
name = "Normal - duplicate values returns first"
inputs = ["3,1,4,1,5", "1"]
expected_output = "1"

[[paradigms]]
paradigm = "structured"
hints = [
    "Add break once found, put the logic in def linear_search(items, target): returning -1 explicitly.",
]
code = '''
def linear_search(items, target):
    for index, value in enumerate(items):
        if value == target:
            return index
    return -1

items = input().split(",")
target = input()
print(linear_search(items, target))
'''

[[paradigms]]
paradigm = "readable"
hints = [
    "Use descriptive names like items, target, index instead of l, t, x.",
]
code = '''
# Search for the first occurrence of target in a comma-separated list
items = input().split(",")
target = input()

# Walk through the list until we find a match or exhaust all items
found_index = -1
for index, value in enumerate(items):
    if value == target:
        found_index = index
        break  # Stop at the first match

print(found_index)
'''

[[paradigms]]
paradigm = "robust"
hints = [
    "What if the list is empty? What if the target contains a comma? Add validation.",
]
code = '''
def linear_search(items, target):
    if not isinstance(items, list):
        raise TypeError("Items must be a list")
    for index, value in enumerate(items):
        if value == target:
            return index
    return -1

raw = input()
items = raw.split(",") if raw else []
target = input()
print(linear_search(items, target))
'''

[[paradigms]]
paradigm = "oop"
hints = [
    "Create a LinearSearcher class with a search(items, target) method.",
]
code = '''
class LinearSearcher:
    def __init__(self):
        self.last_result = -1

    def search(self, items, target):
        for index, value in enumerate(items):
            if value == target:
                self.last_result = index
                return index
        self.last_result = -1
        return -1

searcher = LinearSearcher()
items = input().split(",")
target = input()
print(searcher.search(items, target))
'''

[[paradigms]]
paradigm = "recursive"
hints = [
    "linear_search(items, target, i=0): if i >= len(items) return -1, if items[i]==target return i, else recurse.",
]
code = '''
def linear_search(items, target, index=0):
    if index >= len(items):
        return -1
    if items[index] == target:
        return index
    return linear_search(items, target, index + 1)

items = input().split(",")
target = input()
print(linear_search(items, target))
'''

[[paradigms]]
paradigm = "minimalist"
hints = [
    "Python's list.index() does this in one call — but you need to handle the ValueError for not found.",
]
code = '''
items, target = input().split(","), input()
print(items.index(target) if target in items else -1)
'''

"""

# Illustrative only
items = input().split(",")
target = input()
for index, value in enumerate(items):
    if value == target:
        print(index)
        break
else:
    print(-1)
