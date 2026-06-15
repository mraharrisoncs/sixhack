"""
[challenge]
id = "challenge_020"
title = "Insertion Sort"
description = "Sort a list using the insertion sort algorithm"
difficulty = "intermediate"
spec_level = "gcse"
topic = "Sorting"
free = true

instructions = '''
Read a comma-separated list of integers and sort it in ascending order using
the insertion sort algorithm. Print the sorted list.

Insertion sort works by building up a sorted section one element at a time:
  - Take each element from the unsorted part
  - Shift larger elements in the sorted part right to make room
  - Insert the element into its correct position

Examples:
  Input: 3,1,4,1,5
  Output: [1, 1, 3, 4, 5]

  Input: 5,4,3,2,1
  Output: [1, 2, 3, 4, 5]

  Input: (blank)
  Output: []
'''

starter_code = '''
line = input().strip()
numbers = list(map(int, line.split(","))) if line else []
# Your code here: sort numbers using insertion sort and print the result
'''

hints = [
    "Debug: Trace [3,1,4] step by step — after step 1: [1,3,4], step 2: [1,3,4]. Verify each shift.",
    "Structured: Use a nested loop — outer picks numbers[i], inner shifts elements right while they are larger.",
    "Readable: Use variable names like current_value and insert_position to make the algorithm clear.",
    "Robust: Handle empty lists and single-element lists — insertion sort should return them unchanged.",
    "OOP: Create a Sorter class with a sort() method that performs insertion sort on a stored list.",
    "Recursive: Sort the first n-1 elements recursively, then insert the nth element into its correct position.",
    "Minimalist: Python's built-in sorted() returns a sorted list in one call (though not insertion sort).",
]

[[solutions]]
paradigm = "structured"
code = '''
def insertion_sort(numbers):
    for i in range(1, len(numbers)):
        current = numbers[i]
        j = i - 1
        while j >= 0 and numbers[j] > current:
            numbers[j + 1] = numbers[j]
            j -= 1
        numbers[j + 1] = current
    return numbers

line = input().strip()
numbers = list(map(int, line.split(","))) if line else []
print(insertion_sort(numbers))
'''

[[solutions]]
paradigm = "readable"
code = '''
# Insertion sort: build sorted section left to right
line = input().strip()
numbers = list(map(int, line.split(","))) if line else []

for i in range(1, len(numbers)):
    current_value = numbers[i]
    insert_position = i - 1

    # Shift elements that are larger than current_value to the right
    while insert_position >= 0 and numbers[insert_position] > current_value:
        numbers[insert_position + 1] = numbers[insert_position]
        insert_position -= 1

    # Place current_value in its correct position
    numbers[insert_position + 1] = current_value

print(numbers)
'''

[[solutions]]
paradigm = "robust"
code = '''
def insertion_sort(numbers):
    if not isinstance(numbers, list):
        raise TypeError("Expected a list")
    if len(numbers) <= 1:
        return numbers
    result = numbers[:]
    for i in range(1, len(result)):
        current = result[i]
        j = i - 1
        while j >= 0 and result[j] > current:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = current
    return result

try:
    line = input().strip()
    numbers = list(map(int, line.split(","))) if line else []
    print(insertion_sort(numbers))
except (TypeError, ValueError) as e:
    print(f"Error: {e}")
'''

[[solutions]]
paradigm = "oop"
code = '''
class Sorter:
    def __init__(self, numbers):
        self.numbers = numbers[:]

    def sort(self):
        for i in range(1, len(self.numbers)):
            current = self.numbers[i]
            j = i - 1
            while j >= 0 and self.numbers[j] > current:
                self.numbers[j + 1] = self.numbers[j]
                j -= 1
            self.numbers[j + 1] = current
        return self.numbers

line = input().strip()
numbers = list(map(int, line.split(","))) if line else []
sorter = Sorter(numbers)
print(sorter.sort())
'''

[[solutions]]
paradigm = "recursive"
code = '''
def insert_into_sorted(sorted_list, value):
    if not sorted_list or value <= sorted_list[0]:
        return [value] + sorted_list
    return [sorted_list[0]] + insert_into_sorted(sorted_list[1:], value)

def insertion_sort(numbers):
    if len(numbers) <= 1:
        return numbers
    sorted_part = insertion_sort(numbers[:-1])
    return insert_into_sorted(sorted_part, numbers[-1])

line = input().strip()
numbers = list(map(int, line.split(","))) if line else []
print(insertion_sort(numbers))
'''

[[solutions]]
paradigm = "minimalist"
code = '''
line = input().strip()
print(sorted(map(int, line.split(","))) if line else [])
'''

[[tests]]
paradigm = "all"
name = "Unsorted list"
inputs = ["3,1,4,1,5"]
expected_output = "[1, 1, 3, 4, 5]"

[[tests]]
paradigm = "all"
name = "Reversed list"
inputs = ["5,4,3,2,1"]
expected_output = "[1, 2, 3, 4, 5]"

[[tests]]
paradigm = "all"
name = "Already sorted"
inputs = ["1,2,3,4,5"]
expected_output = "[1, 2, 3, 4, 5]"

[[tests]]
paradigm = "all"
name = "Empty list"
inputs = [""]
expected_output = "[]"

[[tests]]
paradigm = "all"
name = "Single element"
inputs = ["5"]
expected_output = "[5]"
"""

# Illustrative only
line = input().strip()
numbers = list(map(int, line.split(","))) if line else []
for i in range(1, len(numbers)):
    current = numbers[i]
    j = i - 1
    while j >= 0 and numbers[j] > current:
        numbers[j + 1] = numbers[j]
        j -= 1
    numbers[j + 1] = current
print(numbers)
