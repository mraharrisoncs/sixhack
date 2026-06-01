s = input()
o = ""
i = 0
while i < len(s):
    c = s[i]
    n = 1
    while i + n < len(s) and s[i + n] == c:
        n = n + 1
    o = o + str(n) + c
    i = i + n
print(o)

'''!SIX:
description = "Run-length encode a string (e.g. AAABBC -> 3A2B1C)"
instructions = "Input a string of uppercase letters and print its run-length encoding — each group of consecutive identical characters becomes a count followed by the character (e.g. AAABBC → 3A2B1C)."
difficulty = "medium"
topic = "algorithms"
spec_level = "a_level"
hints = ["Debug: Test with AAABBC — you should get 3A2B1C. Try a single repeated character and a single unique character.", "Structure: Extract a helper def count_run(s, start): that returns the run length at a position — separates counting from building the output string."]

[[test_cases]]
number = 1
name = "Normal - mixed runs"
inputs = ["AAABBC"]
expected_output = "3A2B1C\n"

[[test_cases]]
number = 2
name = "Boundary - single character"
inputs = ["A"]
expected_output = "1A\n"

[[test_cases]]
number = 3
name = "Normal - no repeats"
inputs = ["ABCD"]
expected_output = "1A1B1C1D\n"

[[test_cases]]
number = 4
name = "Normal - all same"
inputs = ["AAAAA"]
expected_output = "5A\n"

[[test_cases]]
number = 5
name = "Normal - two runs"
inputs = ["AABB"]
expected_output = "2A2B\n"

[[solutions]]
label = "Clean"
code = """
data = input()
result = ""
index = 0
while index < len(data):
    char = data[index]
    count = 1
    while index + count < len(data) and data[index + count] == char:
        count += 1
    result += str(count) + char
    index += count
print(result)
"""

[[solutions]]
label = "Structured"
code = """
def count_run(data, start):
    char = data[start]
    count = 1
    while start + count < len(data) and data[start + count] == char:
        count += 1
    return char, count

def rle_encode(data):
    result = ""
    index = 0
    while index < len(data):
        char, count = count_run(data, index)
        result += str(count) + char
        index += count
    return result

print(rle_encode(input()))
"""
!SIX.'''
