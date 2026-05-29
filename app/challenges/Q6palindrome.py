'''!SIX:
description = "Check if a word is a palindrome"
difficulty = "medium"

[[test_cases]]
number = 1
name = "Normal - palindrome"
inputs = ["racecar"]
expected_output = "Yes\n"

[[test_cases]]
number = 2
name = "Normal - not palindrome"
inputs = ["hello"]
expected_output = "No\n"

[[test_cases]]
number = 3
name = "Boundary - single character"
inputs = ["a"]
expected_output = "Yes\n"

[[test_cases]]
number = 4
name = "Boundary - two matching"
inputs = ["aa"]
expected_output = "Yes\n"

[[test_cases]]
number = 5
name = "Boundary - two different"
inputs = ["ab"]
expected_output = "No\n"

[[test_cases]]
number = 6
name = "Normal - longer palindrome"
inputs = ["madam"]
expected_output = "Yes\n"
!SIX.'''
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
