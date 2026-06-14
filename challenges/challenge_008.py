"""
[challenge]
id = "challenge_008"
title = "Caesar Cipher"
description = "Encode a lowercase message with a Caesar cipher"
difficulty = "intermediate"
spec_level = "gcse"
topic = "Strings"
free = true

instructions = '''
Input a lowercase message and a shift value, then output the message encoded using
a Caesar cipher (each letter shifted forward by the given amount, wrapping at z).

Examples:
  Input: hello, 3   Output: khoor
  Input: xyz, 3     Output: abc
  Input: python, 0  Output: python
'''

starter_code = '''
msg = input()
s = int(input())
out = ""
i = 0
while i < len(msg):
    c = msg[i]
    n = ord(c)
    n = n - 97
    n = n + s
    n = n % 26
    n = n + 97
    out = out + chr(n)
    i = i + 1
print(out)
'''

hints = [
    "Debug: Try message abc with shift 1 — you should get bcd. Try shift 25 and shift 0 too.",
    "Debug: The magic number 97 is ord('a') — naming it makes the code clearer.",
    "Structured: Put the encoding in def encode(message, shift): — use a for loop over characters rather than while with index.",
    "Readable: Use ord('a') instead of 97, and descriptive names like char_code, shifted_code.",
    "Robust: What if the message contains spaces, digits, or uppercase letters? Add a check or skip non-lowercase characters.",
    "OOP: Create a CaesarCipher class with encode(message, shift) and decode(message, shift) methods.",
    "Recursive: encode(message, shift) = encode_char(message[0], shift) + encode(message[1:], shift), base case empty string.",
    "Minimalist: A join + generator expression encodes the whole string in one line.",
]

[[solutions]]
paradigm = "structured"
code = '''
def encode_char(char, shift):
    return chr((ord(char) - ord("a") + shift) % 26 + ord("a"))

def encode(message, shift):
    return "".join(encode_char(c, shift) for c in message)

message = input()
shift = int(input())
print(encode(message, shift))
'''

[[solutions]]
paradigm = "readable"
code = '''
# Caesar cipher: shift each letter forward in the alphabet, wrapping around
ALPHABET_START = ord("a")
ALPHABET_SIZE = 26

message = input()
shift = int(input())

encoded = ""
for character in message:
    # Convert to 0-25 position, shift, wrap, convert back to letter
    position = ord(character) - ALPHABET_START
    shifted_position = (position + shift) % ALPHABET_SIZE
    encoded += chr(shifted_position + ALPHABET_START)

print(encoded)
'''

[[solutions]]
paradigm = "robust"
code = '''
def encode(message, shift):
    if not isinstance(message, str):
        raise TypeError("Message must be a string")
    if not isinstance(shift, int):
        raise TypeError("Shift must be an integer")
    if not all(c.islower() for c in message):
        raise ValueError("Message must contain only lowercase letters")
    return "".join(
        chr((ord(c) - ord("a") + shift) % 26 + ord("a"))
        for c in message
    )

message = input()
try:
    shift = int(input())
    print(encode(message, shift))
except ValueError as e:
    print(f"Error: {e}")
'''

[[solutions]]
paradigm = "oop"
code = '''
class CaesarCipher:
    def __init__(self):
        self.last_shift = 0

    def encode(self, message, shift):
        self.last_shift = shift
        return "".join(
            chr((ord(c) - ord("a") + shift) % 26 + ord("a"))
            for c in message
        )

    def decode(self, message, shift):
        return self.encode(message, -shift)

cipher = CaesarCipher()
message = input()
shift = int(input())
print(cipher.encode(message, shift))
'''

[[solutions]]
paradigm = "recursive"
code = '''
def encode(message, shift):
    if not message:
        return ""
    head = chr((ord(message[0]) - ord("a") + shift) % 26 + ord("a"))
    return head + encode(message[1:], shift)

message = input()
shift = int(input())
print(encode(message, shift))
'''

[[solutions]]
paradigm = "minimalist"
code = '''
msg, s = input(), int(input())
print("".join(chr((ord(c)-97+s)%26+97) for c in msg))
'''

[[tests]]
paradigm = "all"
name = "Normal"
inputs = ["hello", "3"]
expected_output = "khoor"

[[tests]]
paradigm = "all"
name = "Boundary - wrap around z to a"
inputs = ["xyz", "3"]
expected_output = "abc"

[[tests]]
paradigm = "all"
name = "Boundary - zero shift"
inputs = ["python", "0"]
expected_output = "python"

[[tests]]
paradigm = "all"
name = "Normal - full alphabet"
inputs = ["abcdefghijklmnopqrstuvwxyz", "1"]
expected_output = "bcdefghijklmnopqrstuvwxyza"

[[tests]]
paradigm = "all"
name = "Normal - ROT13"
inputs = ["hello", "13"]
expected_output = "uryyb"
"""

# Illustrative only
msg = input()
s = int(input())
print("".join(chr((ord(c) - 97 + s) % 26 + 97) for c in msg))
