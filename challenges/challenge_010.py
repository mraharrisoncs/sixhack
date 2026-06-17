"""
[challenge]
id = "challenge_010"
title = "Binary Search"
description = "Binary search: find the index of a target in a sorted list"
difficulty = "intermediate"
spec_level = "gcse"
topic = "Searching"
free = true

instructions = '''
Input a sorted comma-separated list of integers and a target, then use binary
search to find and print the index of the target, or -1 if not found.

Binary search works by repeatedly halving the search range:
  - Compare the target to the middle element
  - If equal, return the index
  - If target is smaller, search the left half
  - If target is larger, search the right half

Examples:
  Input: 1,3,5,7,9 then 5   Output: 2
  Input: 1,3,5,7,9 then 4   Output: -1
'''

starter_code = '''
nums = list(map(int, input().split(",")))
target = int(input())
low = 0
high = len(nums)
found = False
while low < high:
    mid = (low + high) // 2
    if nums[mid] == target:
        print(mid)
        found = True
        break
    elif nums[mid] < target:
        low = mid
    else:
        high = mid
if not found:
    print(-1)
'''

[[paradigms]]
paradigm = "all"
hints = [
    "Search for 7 in the list 1,3,5,7,9 — trace low, high and mid each iteration. Does it terminate?",
    "high should start at len(nums)-1 not len(nums) — initialising to len can access an index past the end.",
    "low = mid causes an infinite loop when mid equals low — use low = mid + 1 to always advance.",
]

[[paradigms.tests]]
name = "Normal - item found middle"
inputs = ["1,3,5,7,9", "5"]
expected_output = "2"

[[paradigms.tests]]
name = "Normal - item not found"
inputs = ["1,3,5,7,9", "4"]
expected_output = "-1"

[[paradigms.tests]]
name = "Boundary - first element"
inputs = ["1,3,5,7,9", "1"]
expected_output = "0"

[[paradigms.tests]]
name = "Boundary - last element"
inputs = ["1,3,5,7,9", "9"]
expected_output = "4"

[[paradigms.tests]]
name = "Normal - two elements found"
inputs = ["4,8", "8"]
expected_output = "1"

[[paradigms]]
paradigm = "structured"
hints = [
    "Wrap the binary search in def binary_search(nums, target): returning the index or -1.",
]
code = '''
def binary_search(nums, target):
    low = 0
    high = len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

nums = list(map(int, input().split(",")))
target = int(input())
print(binary_search(nums, target))
'''

[[paradigms]]
paradigm = "readable"
hints = [
    "Use descriptive names like low_index, high_index, mid_index instead of low, high, mid.",
]
code = '''
# Binary search: repeatedly halve the search range
nums = list(map(int, input().split(",")))
target = int(input())

low_index = 0
high_index = len(nums) - 1

while low_index <= high_index:
    mid_index = (low_index + high_index) // 2
    mid_value = nums[mid_index]

    if mid_value == target:
        print(mid_index)
        break
    elif mid_value < target:
        # Target is in the right half
        low_index = mid_index + 1
    else:
        # Target is in the left half
        high_index = mid_index - 1
else:
    print(-1)
'''

[[paradigms]]
paradigm = "robust"
hints = [
    "What if the list is not sorted? Add a check or document that the input must be sorted.",
]
code = '''
def binary_search(nums, target):
    if not nums:
        return -1
    if nums != sorted(nums):
        raise ValueError("List must be sorted for binary search")
    low, high = 0, len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

try:
    nums = list(map(int, input().split(",")))
    target = int(input())
    print(binary_search(nums, target))
except ValueError as e:
    print(f"Error: {e}")
'''

[[paradigms]]
paradigm = "oop"
hints = [
    "Create a BinarySearcher class that stores the sorted list and has a search(target) method.",
]
code = '''
class BinarySearcher:
    def __init__(self, sorted_list):
        self.data = sorted_list

    def search(self, target):
        low, high = 0, len(self.data) - 1
        while low <= high:
            mid = (low + high) // 2
            if self.data[mid] == target:
                return mid
            elif self.data[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return -1

nums = list(map(int, input().split(",")))
target = int(input())
searcher = BinarySearcher(nums)
print(searcher.search(target))
'''

[[paradigms]]
paradigm = "recursive"
hints = [
    "binary_search(nums, target, low, high) with base case low > high returns -1.",
]
code = '''
def binary_search(nums, target, low, high):
    if low > high:
        return -1
    mid = (low + high) // 2
    if nums[mid] == target:
        return mid
    elif nums[mid] < target:
        return binary_search(nums, target, mid + 1, high)
    return binary_search(nums, target, low, mid - 1)

nums = list(map(int, input().split(",")))
target = int(input())
print(binary_search(nums, target, 0, len(nums) - 1))
'''

[[paradigms]]
paradigm = "minimalist"
code = '''
n = list(map(int, input().split(",")))
t, l, h = int(input()), 0, len(n)-1
while l <= h:
    m = (l+h)//2
    if n[m]==t: print(m); break
    elif n[m]<t: l=m+1
    else: h=m-1
else: print(-1)
'''

"""

# Illustrative only
nums = list(map(int, input().split(",")))
target = int(input())
low, high = 0, len(nums) - 1
while low <= high:
    mid = (low + high) // 2
    if nums[mid] == target:
        print(mid)
        break
    elif nums[mid] < target:
        low = mid + 1
    else:
        high = mid - 1
else:
    print(-1)
