"""
[challenge]
id = "challenge_022"
title = "Dice Game Simulator"
description = "Simulate rolling a die and count how many times each face appears"
difficulty = "beginner"
spec_level = "gcse"
topic = "Algorithms"
free = true

instructions = '''
Simulate rolling a 6-sided die and count how many times each face (1-6) appears.

Input:
  Line 1: number of rolls
  Line 2: random seed (integer, for reproducible results)

Output: a list of 6 counts — how many times face 1, 2, 3, 4, 5, 6 each appeared.

Examples:
  Input: 0 rolls, seed 0
  Output: [0, 0, 0, 0, 0, 0]

  Input: 6 rolls, seed 42
  Output: [varies — the six counts sum to 6]

Use random.seed() with the provided seed to make results repeatable.
'''

starter_code = '''
import random

num_rolls = int(input())
seed = int(input())
random.seed(seed)
# Your code here: roll the die num_rolls times and count each face
# Print a list of 6 counts, e.g. [2, 0, 1, 1, 1, 1]
'''

[[paradigms]]
paradigm = "all"
hints = [
    "Use random.randint(1, 6) to roll the die. Print each roll to check it is in the range 1-6.",
]

[[paradigms.tests]]
name = "Zero rolls"
inputs = ["0", "0"]
expected_output = "[0, 0, 0, 0, 0, 0]"

[[paradigms.tests]]
name = "Zero rolls any seed"
inputs = ["0", "99"]
expected_output = "[0, 0, 0, 0, 0, 0]"

[[paradigms]]
paradigm = "structured"
hints = [
    "Create a list counts = [0] * 6. For each roll, do counts[face - 1] += 1.",
]
code = '''
import random

def roll_dice(num_rolls, seed):
    random.seed(seed)
    counts = [0] * 6
    for _ in range(num_rolls):
        face = random.randint(1, 6)
        counts[face - 1] += 1
    return counts

num_rolls = int(input())
seed = int(input())
print(roll_dice(num_rolls, seed))
'''

[[paradigms]]
paradigm = "readable"
hints = [
    "Name variables clearly — face_counts, current_face. A comment explaining the index offset helps.",
]
code = '''
import random

# Simulate rolling a 6-sided die and tally each face
num_rolls = int(input())
seed = int(input())
random.seed(seed)

face_counts = [0, 0, 0, 0, 0, 0]

for roll_number in range(num_rolls):
    current_face = random.randint(1, 6)
    face_counts[current_face - 1] += 1

print(face_counts)
'''

[[paradigms]]
paradigm = "robust"
hints = [
    "Validate num_rolls is non-negative; if zero, all counts should be 0 without entering the loop.",
]
code = '''
import random

def roll_dice(num_rolls, seed):
    if not isinstance(num_rolls, int) or num_rolls < 0:
        raise ValueError("num_rolls must be a non-negative integer")
    random.seed(seed)
    counts = [0] * 6
    for _ in range(num_rolls):
        face = random.randint(1, 6)
        counts[face - 1] += 1
    return counts

try:
    num_rolls = int(input())
    seed = int(input())
    print(roll_dice(num_rolls, seed))
except ValueError as e:
    print(f"Error: {e}")
'''

[[paradigms.tests]]
name = "Single roll seed 0"
inputs = ["1", "0"]
expected_output = "[0, 0, 0, 1, 0, 0]"

[[paradigms]]
paradigm = "oop"
hints = [
    "Create a DiceGame class with roll() and tally() methods. tally() returns the list of face counts.",
]
code = '''
import random

class DiceGame:
    def __init__(self, seed):
        random.seed(seed)
        self._counts = [0] * 6

    def roll(self):
        face = random.randint(1, 6)
        self._counts[face - 1] += 1

    def tally(self):
        return self._counts[:]

num_rolls = int(input())
seed = int(input())
game = DiceGame(seed)
for _ in range(num_rolls):
    game.roll()
print(game.tally())
'''

[[paradigms]]
paradigm = "recursive"
hints = [
    "A recursive roll function accumulates counts list by list — less natural but valid.",
]
code = '''
import random

def roll_recursive(num_rolls, counts):
    if num_rolls == 0:
        return counts
    face = random.randint(1, 6)
    counts[face - 1] += 1
    return roll_recursive(num_rolls - 1, counts)

num_rolls = int(input())
seed = int(input())
random.seed(seed)
print(roll_recursive(num_rolls, [0] * 6))
'''

[[paradigms]]
paradigm = "minimalist"
hints = [
    "Use random.choices() and collections.Counter to count rolls in two lines.",
]
code = '''
import random, collections

num_rolls = int(input())
seed = int(input())
random.seed(seed)
c = collections.Counter(random.choices(range(1, 7), k=num_rolls))
print([c[i] for i in range(1, 7)])
'''

"""

# Illustrative only
import random
num_rolls = int(input())
seed = int(input())
random.seed(seed)
counts = [0] * 6
for _ in range(num_rolls):
    counts[random.randint(1, 6) - 1] += 1
print(counts)
