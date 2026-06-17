"""
[challenge]
id = "challenge_024"
title = "Bit Manipulation"
description = "Perform bitwise AND, OR, XOR, and NOT operations on integers"
difficulty = "intermediate"
spec_level = "a_level"
topic = "Data Representation"
free = false

instructions = '''
Read two integers and an operation name, then perform the bitwise operation.

Operations: AND, OR, XOR, NOT (NOT applies only to the first number)

Input:
  Line 1: integer a
  Line 2: integer b
  Line 3: operation (AND, OR, XOR, or NOT)

Output: the integer result.

Examples:
  5 AND 3 → 1   (binary: 0101 AND 0011 = 0001)
  5 OR  3 → 7   (binary: 0101 OR  0011 = 0111)
  5 XOR 3 → 6   (binary: 0101 XOR 0011 = 0110)
  5 NOT   → -6  (binary: NOT 0101 = ...11111010, two's complement)

Robust: print "Error: Unknown operation" for any other operation name.
'''

starter_code = '''
a = int(input())
b = int(input())
operation = input().strip()
# Your code here: perform the bitwise operation and print the result
'''

[[paradigms]]
paradigm = "all"
hints = [
    "Use bin(5) and bin(3) to see binary — 101 and 011. Work out AND, OR, XOR by hand then verify.",
]

[[paradigms.tests]]
name = "AND operation"
inputs = ["5", "3", "AND"]
expected_output = "1"

[[paradigms.tests]]
name = "OR operation"
inputs = ["5", "3", "OR"]
expected_output = "7"

[[paradigms.tests]]
name = "XOR operation"
inputs = ["5", "3", "XOR"]
expected_output = "6"

[[paradigms.tests]]
name = "AND with zero"
inputs = ["5", "0", "AND"]
expected_output = "0"

[[paradigms.tests]]
name = "NOT operation"
inputs = ["5", "0", "NOT"]
expected_output = "-6"

[[paradigms]]
paradigm = "structured"
hints = [
    "Use if/elif to check the operation name and apply the matching Python bitwise operator.",
]
code = '''
def bitwise(a, b, operation):
    if operation == "AND":
        return a & b
    elif operation == "OR":
        return a | b
    elif operation == "XOR":
        return a ^ b
    elif operation == "NOT":
        return ~a
    else:
        return None

a = int(input())
b = int(input())
operation = input().strip()
result = bitwise(a, b, operation)
if result is None:
    print("Error: Unknown operation")
else:
    print(result)
'''

[[paradigms]]
paradigm = "readable"
hints = [
    "Add a comment for each branch explaining what the operator does in binary terms.",
]
code = '''
# Perform a bitwise operation on two integers
a = int(input())
b = int(input())
operation = input().strip()

if operation == "AND":
    # AND: result bit is 1 only if both input bits are 1
    result = a & b
elif operation == "OR":
    # OR: result bit is 1 if either input bit is 1
    result = a | b
elif operation == "XOR":
    # XOR: result bit is 1 only if the input bits differ
    result = a ^ b
elif operation == "NOT":
    # NOT: flip all bits (gives -(a+1) in two's complement)
    result = ~a
else:
    result = None

if result is not None:
    print(result)
else:
    print("Error: Unknown operation")
'''

[[paradigms]]
paradigm = "robust"
hints = [
    "Use a dict mapping operation names to operators, or raise an error for unknown operations.",
]
code = '''
OPERATIONS = {"AND", "OR", "XOR", "NOT"}

def bitwise(a, b, operation):
    if operation not in OPERATIONS:
        raise ValueError(f"Unknown operation: {operation}")
    if operation == "AND":
        return a & b
    if operation == "OR":
        return a | b
    if operation == "XOR":
        return a ^ b
    if operation == "NOT":
        return ~a

try:
    a = int(input())
    b = int(input())
    operation = input().strip().upper()
    print(bitwise(a, b, operation))
except ValueError as e:
    print(f"Error: {e}")
'''

[[paradigms.tests]]
name = "Invalid operation"
inputs = ["5", "3", "NAND"]
expected_output = "Error: Unknown operation"

[[paradigms]]
paradigm = "oop"
hints = [
    "Create a BitwiseCalculator class with methods and(), or_(), xor(), not_() for each operation.",
]
code = '''
class BitwiseCalculator:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def and_(self):
        return self.a & self.b

    def or_(self):
        return self.a | self.b

    def xor(self):
        return self.a ^ self.b

    def not_(self):
        return ~self.a

    def apply(self, operation):
        ops = {"AND": self.and_, "OR": self.or_, "XOR": self.xor, "NOT": self.not_}
        if operation not in ops:
            raise ValueError(f"Unknown operation: {operation}")
        return ops[operation]()

a = int(input())
b = int(input())
operation = input().strip()
calc = BitwiseCalculator(a, b)
try:
    print(calc.apply(operation))
except ValueError as e:
    print(f"Error: {e}")
'''

[[paradigms]]
paradigm = "recursive"
hints = [
    "Shift and combine bits recursively — compute AND bit by bit using >> and &1.",
]
code = '''
def bitwise_and(a, b, bit=0):
    if a == 0 and b == 0:
        return 0
    return ((a & 1) & (b & 1)) << bit | bitwise_and(a >> 1, b >> 1, bit + 1)

def bitwise_or(a, b, bit=0):
    if a == 0 and b == 0:
        return 0
    return ((a & 1) | (b & 1)) << bit | bitwise_or(a >> 1, b >> 1, bit + 1)

def bitwise_xor(a, b, bit=0):
    if a == 0 and b == 0:
        return 0
    return ((a & 1) ^ (b & 1)) << bit | bitwise_xor(a >> 1, b >> 1, bit + 1)

a = int(input())
b = int(input())
operation = input().strip()

if operation == "AND":
    print(bitwise_and(a, b))
elif operation == "OR":
    print(bitwise_or(a, b))
elif operation == "XOR":
    print(bitwise_xor(a, b))
elif operation == "NOT":
    print(~a)
else:
    print("Error: Unknown operation")
'''

[[paradigms]]
paradigm = "minimalist"
hints = [
    "A dict of lambdas maps operation names to one-line results.",
]
code = '''
a, b, op = int(input()), int(input()), input().strip()
ops = {"AND": lambda: a & b, "OR": lambda: a | b, "XOR": lambda: a ^ b, "NOT": lambda: ~a}
print(ops[op]() if op in ops else "Error: Unknown operation")
'''

"""

# Illustrative only
a = int(input())
b = int(input())
op = input().strip()
ops = {"AND": a & b, "OR": a | b, "XOR": a ^ b, "NOT": ~a}
print(ops.get(op, "Error: Unknown operation"))
