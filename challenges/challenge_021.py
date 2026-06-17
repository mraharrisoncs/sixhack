"""
[challenge]
id = "challenge_021"
title = "Merge Sort"
description = "Sort a list using the merge sort algorithm"
difficulty = "intermediate"
spec_level = "a_level"
topic = "Sorting"
free = false

instructions = '''
Read a comma-separated list of integers and sort it in ascending order using
the merge sort algorithm. Print the sorted list.

Merge sort is a divide-and-conquer algorithm:
  1. Divide: split the list in half
  2. Conquer: recursively sort each half
  3. Combine: merge the two sorted halves into one sorted list

Examples:
  Input: 3,1,4,1,5,9
  Output: [1, 1, 3, 4, 5, 9]

  Input: (blank)
  Output: []

  Input: 5
  Output: [5]
'''

starter_code = '''
line = input().strip()
numbers = list(map(int, line.split(","))) if line else []
# Your code here: sort numbers using merge sort and print the result
'''

[[paradigms]]
paradigm = "all"
hints = [
    "Trace [3,1,4] — split to [3] and [1,4], sort [1,4] to get [1,4], then merge [3] and [1,4].",
]

[[paradigms.tests]]
name = "Unsorted list"
inputs = ["3,1,4,1,5,9"]
expected_output = "[1, 1, 3, 4, 5, 9]"

[[paradigms.tests]]
name = "Empty list"
inputs = [""]
expected_output = "[]"

[[paradigms.tests]]
name = "Single element"
inputs = ["5"]
expected_output = "[5]"

[[paradigms.tests]]
name = "Already sorted"
inputs = ["1,2,3,4,5"]
expected_output = "[1, 2, 3, 4, 5]"

[[paradigms.tests]]
name = "Duplicates"
inputs = ["2,2,1,1,3"]
expected_output = "[1, 1, 2, 2, 3]"

[[paradigms]]
paradigm = "structured"
hints = [
    "Write a merge(left, right) helper that combines two sorted lists, then a sort function that calls it.",
]
code = '''
def merge(left, right):
    result = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def merge_sort(numbers):
    if len(numbers) <= 1:
        return numbers
    mid = len(numbers) // 2
    left = merge_sort(numbers[:mid])
    right = merge_sort(numbers[mid:])
    return merge(left, right)

line = input().strip()
numbers = list(map(int, line.split(","))) if line else []
print(merge_sort(numbers))
'''

[[paradigms]]
paradigm = "readable"
hints = [
    "Use clear variable names; separate merge logic from divide logic with well-named functions.",
]
code = '''
# Merge sort: divide the list, sort each half, then merge

def merge_sorted_halves(left_half, right_half):
    merged = []
    left_index = 0
    right_index = 0

    # Compare elements from each half and take the smaller one
    while left_index < len(left_half) and right_index < len(right_half):
        if left_half[left_index] <= right_half[right_index]:
            merged.append(left_half[left_index])
            left_index += 1
        else:
            merged.append(right_half[right_index])
            right_index += 1

    # Append any remaining elements from either half
    merged.extend(left_half[left_index:])
    merged.extend(right_half[right_index:])
    return merged

def merge_sort(numbers):
    if len(numbers) <= 1:
        return numbers
    midpoint = len(numbers) // 2
    left_sorted = merge_sort(numbers[:midpoint])
    right_sorted = merge_sort(numbers[midpoint:])
    return merge_sorted_halves(left_sorted, right_sorted)

line = input().strip()
numbers = list(map(int, line.split(","))) if line else []
print(merge_sort(numbers))
'''

[[paradigms]]
paradigm = "robust"
hints = [
    "Handle the base cases — an empty list or single-element list is already sorted, return it as-is.",
]
code = '''
def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    return result + left[i:] + right[j:]

def merge_sort(numbers):
    if not isinstance(numbers, list):
        raise TypeError("Expected a list")
    if len(numbers) <= 1:
        return numbers[:]
    mid = len(numbers) // 2
    return merge(merge_sort(numbers[:mid]), merge_sort(numbers[mid:]))

try:
    line = input().strip()
    numbers = list(map(int, line.split(","))) if line else []
    print(merge_sort(numbers))
except (TypeError, ValueError) as e:
    print(f"Error: {e}")
'''

[[paradigms]]
paradigm = "oop"
hints = [
    "Create a MergeSorter class with sort() and merge() methods; sort() calls itself recursively.",
]
code = '''
class MergeSorter:
    def merge(self, left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        return result + left[i:] + right[j:]

    def sort(self, numbers):
        if len(numbers) <= 1:
            return numbers
        mid = len(numbers) // 2
        left = self.sort(numbers[:mid])
        right = self.sort(numbers[mid:])
        return self.merge(left, right)

line = input().strip()
numbers = list(map(int, line.split(","))) if line else []
sorter = MergeSorter()
print(sorter.sort(numbers))
'''

[[paradigms]]
paradigm = "recursive"
hints = [
    "merge_sort(numbers) returns numbers if len <= 1, else merges merge_sort(left) and merge_sort(right).",
]
code = '''
def merge_sort(numbers):
    if len(numbers) <= 1:
        return numbers
    mid = len(numbers) // 2
    left = merge_sort(numbers[:mid])
    right = merge_sort(numbers[mid:])
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    return merged + left[i:] + right[j:]

line = input().strip()
numbers = list(map(int, line.split(","))) if line else []
print(merge_sort(numbers))
'''

[[paradigms]]
paradigm = "minimalist"
hints = [
    "The recursive approach can be written compactly, but clarity matters more than brevity here.",
]
code = '''
def ms(n):
    if len(n) <= 1: return n
    m = len(n)//2
    l, r = ms(n[:m]), ms(n[m:])
    res, i, j = [], 0, 0
    while i < len(l) and j < len(r):
        if l[i] <= r[j]: res.append(l[i]); i += 1
        else: res.append(r[j]); j += 1
    return res + l[i:] + r[j:]

line = input().strip()
print(ms(list(map(int, line.split(",")))) if line else [])
'''

"""

# Illustrative only
line = input().strip()
numbers = list(map(int, line.split(","))) if line else []

def merge_sort(n):
    if len(n) <= 1: return n
    m = len(n) // 2
    l, r = merge_sort(n[:m]), merge_sort(n[m:])
    res, i, j = [], 0, 0
    while i < len(l) and j < len(r):
        if l[i] <= r[j]: res.append(l[i]); i += 1
        else: res.append(r[j]); j += 1
    return res + l[i:] + r[j:]

print(merge_sort(numbers))
