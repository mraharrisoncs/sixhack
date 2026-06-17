"""
[challenge]
id = "challenge_011"
title = "Bubble Sort"
description = "Bubble sort: sort a list and print the list after each pass"
difficulty = "intermediate"
spec_level = "gcse"
topic = "Sorting"
free = true

instructions = '''
Input a comma-separated list of integers and sort it using bubble sort,
printing the state of the list after every pass.

Example (input: 4,2,7,1):
  2,4,1,7
  2,1,4,7
  1,2,4,7
  1,2,4,7
'''

starter_code = '''
nums = list(map(int, input().split(",")))
n = len(nums)
for i in range(n):
    for j in range(n - 1):
        if nums[j] > nums[j + 1]:
            t = nums[j]
            nums[j] = nums[j + 1]
            nums[j + 1] = t
    print(",".join(map(str, nums)))
'''

[[paradigms]]
paradigm = "all"
hints = [
    "Run with [4,3,2,1] and count lines of output — are there too many passes?",
    "The inner loop range should shrink each pass (range(n-1-i)) since sorted elements settle at the end.",
]

[[paradigms.tests]]
name = "Normal - four elements"
inputs = ["4,2,7,1"]
expected_output = "2,4,1,7\n2,1,4,7\n1,2,4,7\n1,2,4,7"

[[paradigms.tests]]
name = "Boundary - already sorted"
inputs = ["1,2,3"]
expected_output = "1,2,3\n1,2,3\n1,2,3"

[[paradigms.tests]]
name = "Boundary - two elements"
inputs = ["5,1"]
expected_output = "1,5\n1,5"

[[paradigms.tests]]
name = "Normal - reverse sorted"
inputs = ["3,2,1"]
expected_output = "2,1,3\n1,2,3\n1,2,3"

[[paradigms]]
paradigm = "structured"
hints = [
    "Wrap the sort in def bubble_sort(nums): and use Python's tuple swap (a, b = b, a).",
]
code = '''
def bubble_sort(nums):
    n = len(nums)
    for i in range(n):
        for j in range(n - 1 - i):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
        print(",".join(map(str, nums)))

nums = list(map(int, input().split(",")))
bubble_sort(nums)
'''

[[paradigms]]
paradigm = "readable"
hints = [
    "Name the outer loop variable pass_number and inner loop variable comparison_index.",
]
code = '''
# Bubble sort: larger values "bubble up" to the right each pass
nums = list(map(int, input().split(",")))
total_elements = len(nums)

for pass_number in range(total_elements):
    # Each pass, the last (pass_number) elements are already in place
    for comparison_index in range(total_elements - 1 - pass_number):
        left = nums[comparison_index]
        right = nums[comparison_index + 1]
        if left > right:
            # Swap the two adjacent elements
            nums[comparison_index], nums[comparison_index + 1] = right, left
    print(",".join(map(str, nums)))
'''

[[paradigms]]
paradigm = "robust"
hints = [
    "What if the list has only one element? What if it is already sorted? Add an early-exit flag.",
]
code = '''
def bubble_sort(nums):
    if not isinstance(nums, list):
        raise TypeError("Input must be a list")
    if not all(isinstance(x, int) for x in nums):
        raise TypeError("All elements must be integers")
    n = len(nums)
    result = nums[:]
    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        print(",".join(map(str, result)))
        if not swapped:
            break
    return result

try:
    nums = list(map(int, input().split(",")))
    bubble_sort(nums)
except ValueError:
    print("Error: all elements must be integers")
'''

[[paradigms]]
paradigm = "oop"
hints = [
    "Create a BubbleSorter class with a sort(nums) method that returns each intermediate state.",
]
code = '''
class BubbleSorter:
    def __init__(self):
        self.passes = []

    def sort(self, nums):
        data = nums[:]
        n = len(data)
        self.passes = []
        for i in range(n):
            for j in range(n - 1 - i):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
            self.passes.append(data[:])
        return data

sorter = BubbleSorter()
nums = list(map(int, input().split(",")))
sorter.sort(nums)
for state in sorter.passes:
    print(",".join(map(str, state)))
'''

[[paradigms]]
paradigm = "recursive"
hints = [
    "Not a natural fit for bubble sort, but try defining one pass as a recursive helper.",
]
code = '''
def bubble_pass(nums, end):
    if end == 0:
        return
    for j in range(end):
        if nums[j] > nums[j + 1]:
            nums[j], nums[j + 1] = nums[j + 1], nums[j]
    print(",".join(map(str, nums)))
    bubble_pass(nums, end - 1)

nums = list(map(int, input().split(",")))
bubble_pass(nums, len(nums) - 1)
'''

[[paradigms]]
paradigm = "minimalist"
hints = [
    "Use Python's built-in sort — though that defeats the purpose of learning the algorithm.",
]
code = '''
n = list(map(int, input().split(",")))
[print(",".join(map(str, n))) for i in range(len(n)) for j in range(len(n)-1-i) if n[j]>n[j+1] and n.__setitem__(slice(j,j+2),[n[j+1],n[j]]) or False] or [print(",".join(map(str,n)))]
'''

"""

# Illustrative only
nums = list(map(int, input().split(",")))
n = len(nums)
for i in range(n):
    for j in range(n - 1 - i):
        if nums[j] > nums[j + 1]:
            nums[j], nums[j + 1] = nums[j + 1], nums[j]
    print(",".join(map(str, nums)))
