w = int(input())
h = int(input())
d = int(input())
s = w * h * d
print(s)

'''!SIX:
description = "Calculate the file size of an uncompressed bitmap image in bytes"
difficulty = "easy"
topic = "data representation"
spec_level = "gcse"
hints = ["Width x height x colour depth gives you bits, not bytes", "Variable names w, h, d, s are not self-documenting", "What are the units of colour depth — bits per pixel"]

[[test_cases]]
number = 1
name = "Normal - 24-bit colour 100x100"
inputs = [100, 100, 24]
expected_output = "30000\n"

[[test_cases]]
number = 2
name = "Boundary - 1x1 pixel 8-bit"
inputs = [1, 1, 8]
expected_output = "1\n"

[[test_cases]]
number = 3
name = "Normal - 1920x1080 24-bit"
inputs = [1920, 1080, 24]
expected_output = "6220800\n"

[[test_cases]]
number = 4
name = "Normal - 640x480 1-bit"
inputs = [640, 480, 1]
expected_output = "38400\n"

[[solutions]]
label = "Clean"
code = """
width = int(input())
height = int(input())
colour_depth = int(input())
bits = width * height * colour_depth
file_size_bytes = bits // 8
print(file_size_bytes)
"""

[[solutions]]
label = "Structured"
code = """
def bitmap_size_bytes(width, height, colour_depth):
    return (width * height * colour_depth) // 8

width = int(input())
height = int(input())
colour_depth = int(input())
print(bitmap_size_bytes(width, height, colour_depth))
"""
!SIX.'''
