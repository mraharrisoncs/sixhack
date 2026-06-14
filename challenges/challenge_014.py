"""
[challenge]
id = "challenge_014"
title = "Bitmap File Size"
description = "Calculate the file size of an uncompressed bitmap image in bytes"
difficulty = "beginner"
spec_level = "gcse"
topic = "Data Representation"
free = false

instructions = '''
Input the width (pixels), height (pixels), and colour depth (bits per pixel)
of an image, then calculate and print the uncompressed file size in bytes.

Formula: file_size = (width * height * colour_depth) / 8

Examples:
  Input: 100, 100, 24   Output: 30000
  Input: 1920, 1080, 24 Output: 6220800
  Input: 1, 1, 8        Output: 1
'''

starter_code = '''
w = int(input())
h = int(input())
d = int(input())
s = w * h * d
print(s)
'''

hints = [
    "Debug: Test with width=100, height=100, depth=24 — expected 30000 bytes. What does this code output, and why?",
    "Bug: width x height x depth gives bits not bytes — you need to divide by 8 to convert.",
    "Structured: Wrap the calculation in def bitmap_size(width, height, colour_depth): and keep input in the main block.",
    "Readable: Use BITS_PER_BYTE = 8 as a named constant instead of dividing by the magic number 8.",
    "Robust: What if width or height is zero? What if colour_depth is not a power of 2? Add validation.",
    "OOP: Create an Image class with width, height, colour_depth attributes and a file_size() method.",
    "Recursive: Not natural here, but you could compute width*height by repeated addition recursively.",
    "Minimalist: The formula fits on one line — no intermediate variables needed.",
]

[[solutions]]
paradigm = "structured"
code = '''
BITS_PER_BYTE = 8

def bitmap_size(width, height, colour_depth):
    return (width * height * colour_depth) // BITS_PER_BYTE

width = int(input())
height = int(input())
colour_depth = int(input())
print(bitmap_size(width, height, colour_depth))
'''

[[solutions]]
paradigm = "readable"
code = '''
# Calculate uncompressed bitmap size using the standard formula
BITS_PER_BYTE = 8

width = int(input())
height = int(input())
colour_depth = int(input())

# Total bits = pixels * bits per pixel
total_pixels = width * height
total_bits = total_pixels * colour_depth

# Convert bits to bytes
file_size_bytes = total_bits // BITS_PER_BYTE
print(file_size_bytes)
'''

[[solutions]]
paradigm = "robust"
code = '''
BITS_PER_BYTE = 8
VALID_DEPTHS = {1, 4, 8, 16, 24, 32}

def bitmap_size(width, height, colour_depth):
    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be positive")
    if colour_depth not in VALID_DEPTHS:
        raise ValueError(f"Colour depth must be one of {sorted(VALID_DEPTHS)}")
    return (width * height * colour_depth) // BITS_PER_BYTE

try:
    width = int(input())
    height = int(input())
    colour_depth = int(input())
    print(bitmap_size(width, height, colour_depth))
except ValueError as e:
    print(f"Error: {e}")
'''

[[solutions]]
paradigm = "oop"
code = '''
class Image:
    BITS_PER_BYTE = 8

    def __init__(self, width, height, colour_depth):
        self.width = width
        self.height = height
        self.colour_depth = colour_depth

    def file_size(self):
        return (self.width * self.height * self.colour_depth) // self.BITS_PER_BYTE

width = int(input())
height = int(input())
colour_depth = int(input())
image = Image(width, height, colour_depth)
print(image.file_size())
'''

[[solutions]]
paradigm = "recursive"
code = '''
BITS_PER_BYTE = 8

def multiply(a, b):
    if b == 0:
        return 0
    return a + multiply(a, b - 1)

def bitmap_size(width, height, colour_depth):
    total_pixels = multiply(width, height)
    total_bits = multiply(total_pixels, colour_depth)
    return total_bits // BITS_PER_BYTE

width = int(input())
height = int(input())
colour_depth = int(input())
print(bitmap_size(width, height, colour_depth))
'''

[[solutions]]
paradigm = "minimalist"
code = '''
print(int(input())*int(input())*int(input())//8)
'''

[[tests]]
paradigm = "all"
name = "Normal - 24-bit colour 100x100"
inputs = ["100", "100", "24"]
expected_output = "30000"

[[tests]]
paradigm = "all"
name = "Boundary - 1x1 pixel 8-bit"
inputs = ["1", "1", "8"]
expected_output = "1"

[[tests]]
paradigm = "all"
name = "Normal - 1920x1080 24-bit"
inputs = ["1920", "1080", "24"]
expected_output = "6220800"

[[tests]]
paradigm = "all"
name = "Normal - 640x480 1-bit"
inputs = ["640", "480", "1"]
expected_output = "38400"
"""

# Illustrative only
w = int(input())
h = int(input())
d = int(input())
print(w * h * d // 8)
