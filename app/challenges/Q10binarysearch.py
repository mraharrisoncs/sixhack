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

'''!SIX:
description = "Binary search: find the index of a target in a sorted list"
instructions = "Input a sorted comma-separated list of integers and a target, then use binary search to find and print the index of the target, or -1 if not found."
difficulty = "medium"
topic = "searching"
spec_level = "gcse"
hints = ["Debug: Search for 7 in the list 1,3,5,7,9 — trace low, high and mid each iteration. Does it terminate?", "Bug: high should start at len(nums)-1, not len(nums) — it can read past the end of the list.", "Bug: low = mid causes an infinite loop when mid equals low — use low = mid + 1."]

[[test_cases]]
number = 1
name = "Normal - item found middle"
inputs = ["1,3,5,7,9", "5"]
expected_output = "2\n"

[[test_cases]]
number = 2
name = "Normal - item not found"
inputs = ["1,3,5,7,9", "4"]
expected_output = "-1\n"

[[test_cases]]
number = 3
name = "Boundary - first element"
inputs = ["1,3,5,7,9", "1"]
expected_output = "0\n"

[[test_cases]]
number = 4
name = "Boundary - last element"
inputs = ["1,3,5,7,9", "9"]
expected_output = "4\n"

[[test_cases]]
number = 5
name = "Normal - two elements found"
inputs = ["4,8", "8"]
expected_output = "1\n"

[[solutions]]
label = "Clean"
code = """
nums = list(map(int, input().split(",")))
target = int(input())
low = 0
high = len(nums) - 1
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
"""

[[solutions]]
label = "Structured"
code = """
def binary_search(nums, target):
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

nums = list(map(int, input().split(",")))
target = int(input())
print(binary_search(nums, target))
"""
!SIX.'''
