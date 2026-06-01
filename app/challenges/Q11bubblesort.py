nums = list(map(int, input().split(",")))
n = len(nums)
for i in range(n):
    for j in range(n - 1):
        if nums[j] > nums[j + 1]:
            t = nums[j]
            nums[j] = nums[j + 1]
            nums[j + 1] = t
    print(",".join(map(str, nums)))

'''!SIX:
description = "Bubble sort: sort a list and print the list after each pass"
instructions = "Input a comma-separated list of integers and sort it using bubble sort, printing the state of the list after every pass."
difficulty = "medium"
topic = "sorting"
spec_level = "gcse"
hints = ["Debug: Run with [4,3,2,1] and count lines of output — are there too many passes?", "Structure: The inner loop range should shrink each pass (range(n-1-i)) since sorted elements settle at the end — wrap the sort in def bubble_sort(nums):."]

[[test_cases]]
number = 1
name = "Normal - four elements"
inputs = ["4,2,7,1"]
expected_output = "2,4,1,7\n2,1,4,7\n1,2,4,7\n1,2,4,7\n"

[[test_cases]]
number = 2
name = "Boundary - already sorted"
inputs = ["1,2,3"]
expected_output = "1,2,3\n1,2,3\n1,2,3\n"

[[test_cases]]
number = 3
name = "Boundary - two elements"
inputs = ["5,1"]
expected_output = "1,5\n1,5\n"

[[test_cases]]
number = 4
name = "Normal - reverse sorted"
inputs = ["3,2,1"]
expected_output = "2,1,3\n1,2,3\n1,2,3\n"

[[solutions]]
label = "Clean"
code = """
nums = list(map(int, input().split(",")))
n = len(nums)
for i in range(n):
    for j in range(n - 1 - i):
        if nums[j] > nums[j + 1]:
            nums[j], nums[j + 1] = nums[j + 1], nums[j]
    print(",".join(map(str, nums)))
"""

[[solutions]]
label = "Optimised"
code = """
nums = list(map(int, input().split(",")))
n = len(nums)
for i in range(n):
    swapped = False
    for j in range(n - 1 - i):
        if nums[j] > nums[j + 1]:
            nums[j], nums[j + 1] = nums[j + 1], nums[j]
            swapped = True
    print(",".join(map(str, nums)))
    if not swapped:
        break
"""
!SIX.'''
