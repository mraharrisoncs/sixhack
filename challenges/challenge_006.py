"""
[challenge]
id = "challenge_006"
title = "Palindrome Checker"
description = "Check if a word is a palindrome"
difficulty = "beginner"
spec_level = "gcse"
topic = "Strings"
free = true

instructions = '''
Input a word and print Yes if it reads the same forwards and backwards,
or No if it does not.

Examples:
  Input: racecar  Output: Yes
  Input: hello    Output: No
  Input: a        Output: Yes
'''

starter_code = '''
word = input()
reversed_word = ""
i = 0
while i < len(word):
    reversed_word = word[i] + reversed_word
    i = i + 1
is_palindrome = False
if reversed_word == word:
    is_palindrome = True
if is_palindrome == True:
    print("Yes")
if is_palindrome == False:
    print("No")
'''

hints = [
    "Debug: Test with racecar (Yes) and hello (No). Trace the while loop — is the reversal correct?",
    "Debug: Comparing is_palindrome == True is redundant — just use if is_palindrome: directly.",
    "Structured: Put the palindrome check in def is_palindrome(word): returning True/False — call it from main.",
    "Readable: Python's slice notation word[::-1] reverses a string in one step — no loop needed.",
    "Robust: Should the check be case-sensitive? abBA is a palindrome if you ignore case — add .lower() if needed.",
    "OOP: Create a PalindromeChecker class with a check(word) method returning True/False.",
    "Recursive: A word is a palindrome if the first and last characters match AND the middle is also a palindrome.",
    "Minimalist: The whole check fits in one print statement using Python's slice reversal.",
]

[[solutions]]
paradigm = "structured"
code = '''
def is_palindrome(word):
    return word == word[::-1]

word = input()
print("Yes" if is_palindrome(word) else "No")
'''

[[solutions]]
paradigm = "readable"
code = '''
# Check whether a word reads the same in both directions
word = input()

# Reverse using Python slice notation
reversed_word = word[::-1]

# Compare and report result
if word == reversed_word:
    print("Yes")
else:
    print("No")
'''

[[solutions]]
paradigm = "robust"
code = '''
def is_palindrome(word, case_sensitive=True):
    if not isinstance(word, str):
        raise TypeError("Input must be a string")
    if not word:
        raise ValueError("Input cannot be empty")
    check = word if case_sensitive else word.lower()
    return check == check[::-1]

try:
    word = input()
    print("Yes" if is_palindrome(word) else "No")
except ValueError as e:
    print(f"Error: {e}")
'''

[[solutions]]
paradigm = "oop"
code = '''
class PalindromeChecker:
    def __init__(self):
        self.last_word = None

    def check(self, word):
        self.last_word = word
        return word == word[::-1]

checker = PalindromeChecker()
word = input()
print("Yes" if checker.check(word) else "No")
'''

[[solutions]]
paradigm = "recursive"
code = '''
def is_palindrome(word):
    if len(word) <= 1:
        return True
    if word[0] != word[-1]:
        return False
    return is_palindrome(word[1:-1])

word = input()
print("Yes" if is_palindrome(word) else "No")
'''

[[solutions]]
paradigm = "minimalist"
code = '''
w = input()
print("Yes" if w == w[::-1] else "No")
'''

[[tests]]
paradigm = "all"
name = "Normal - palindrome"
inputs = ["racecar"]
expected_output = "Yes"

[[tests]]
paradigm = "all"
name = "Normal - not palindrome"
inputs = ["hello"]
expected_output = "No"

[[tests]]
paradigm = "all"
name = "Boundary - single character"
inputs = ["a"]
expected_output = "Yes"

[[tests]]
paradigm = "all"
name = "Boundary - two matching"
inputs = ["aa"]
expected_output = "Yes"

[[tests]]
paradigm = "all"
name = "Boundary - two different"
inputs = ["ab"]
expected_output = "No"

[[tests]]
paradigm = "all"
name = "Normal - longer palindrome"
inputs = ["madam"]
expected_output = "Yes"
"""

# Illustrative only
word = input()
print("Yes" if word == word[::-1] else "No")
