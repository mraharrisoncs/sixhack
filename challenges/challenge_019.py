"""
[challenge]
id = "challenge_019"
title = "Matrix Transpose"
description = "Transpose a 2D matrix (swap rows and columns)"
difficulty = "intermediate"
spec_level = "gcse"
topic = "Arrays"
free = true

instructions = '''
Read a matrix and print its transpose (rows and columns swapped).

Input format:
  First line: number of rows N
  Next N lines: comma-separated integers for each row

Output: the transposed matrix as a Python list of lists.

Examples:
  Input: 2 rows, then "1,2" and "3,4"
  Output: [[1, 3], [2, 4]]

  Input: 2 rows, then "1,2,3" and "4,5,6"
  Output: [[1, 4], [2, 5], [3, 6]]
'''

starter_code = '''
n = int(input())
matrix = [list(map(int, input().split(","))) for _ in range(n)]
# Your code here: transpose the matrix and print the result
'''

hints = [
    "Debug: Trace the 2x2 case [[1,2],[3,4]] — row 0 col 1 becomes row 1 col 0 in the transpose.",
    "Structured: Use a helper function build_transposed(matrix) with nested loops: outer over columns, inner over rows.",
    "Readable: Name your variables num_rows and num_cols; build each transposed row with a list comprehension.",
    "Robust: Check the matrix is not empty and all rows have equal length before transposing.",
    "OOP: Create a Matrix class storing the grid, with a transpose() method that returns a new Matrix.",
    "Recursive: Build the first column as a new row, then recurse on the matrix with that column removed.",
    "Minimalist: zip(*matrix) gives the transposed columns — wrap each in list() to get the result.",
]

[[solutions]]
paradigm = "structured"
code = '''
def build_transposed(matrix):
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    result = []
    for c in range(num_cols):
        new_row = []
        for r in range(num_rows):
            new_row.append(matrix[r][c])
        result.append(new_row)
    return result

n = int(input())
matrix = [list(map(int, input().split(","))) for _ in range(n)]
print(build_transposed(matrix))
'''

[[solutions]]
paradigm = "readable"
code = '''
# Transpose a matrix by swapping rows and columns
n = int(input())
matrix = [list(map(int, input().split(","))) for _ in range(n)]

num_rows = len(matrix)
num_cols = len(matrix[0])

transposed = []
for col_index in range(num_cols):
    # Build a new row from each row's element at col_index
    new_row = [matrix[row_index][col_index] for row_index in range(num_rows)]
    transposed.append(new_row)

print(transposed)
'''

[[solutions]]
paradigm = "robust"
code = '''
def transpose(matrix):
    if not matrix:
        return []
    row_length = len(matrix[0])
    for row in matrix:
        if len(row) != row_length:
            raise ValueError("All rows must have equal length")
    num_rows = len(matrix)
    num_cols = row_length
    return [[matrix[r][c] for r in range(num_rows)] for c in range(num_cols)]

try:
    n = int(input())
    matrix = [list(map(int, input().split(","))) for _ in range(n)]
    print(transpose(matrix))
except ValueError as e:
    print(f"Error: {e}")
'''

[[solutions]]
paradigm = "oop"
code = '''
class Matrix:
    def __init__(self, grid):
        self.grid = grid

    def transpose(self):
        num_rows = len(self.grid)
        num_cols = len(self.grid[0])
        transposed = [[self.grid[r][c] for r in range(num_rows)] for c in range(num_cols)]
        return Matrix(transposed)

    def __repr__(self):
        return str(self.grid)

n = int(input())
grid = [list(map(int, input().split(","))) for _ in range(n)]
m = Matrix(grid)
print(m.transpose())
'''

[[solutions]]
paradigm = "recursive"
code = '''
def transpose(matrix):
    if not matrix or not matrix[0]:
        return []
    first_col = [row[0] for row in matrix]
    rest = transpose([row[1:] for row in matrix])
    return [first_col] + rest

n = int(input())
matrix = [list(map(int, input().split(","))) for _ in range(n)]
print(transpose(matrix))
'''

[[solutions]]
paradigm = "minimalist"
code = '''
n = int(input())
m = [list(map(int, input().split(","))) for _ in range(n)]
print([list(col) for col in zip(*m)])
'''

[[tests]]
paradigm = "all"
name = "2x2 square matrix"
inputs = ["2", "1,2", "3,4"]
expected_output = "[[1, 3], [2, 4]]"

[[tests]]
paradigm = "all"
name = "2x3 rectangle"
inputs = ["2", "1,2,3", "4,5,6"]
expected_output = "[[1, 4], [2, 5], [3, 6]]"

[[tests]]
paradigm = "all"
name = "Single row matrix"
inputs = ["1", "1,2,3"]
expected_output = "[[1], [2], [3]]"

[[tests]]
paradigm = "all"
name = "3x3 square matrix"
inputs = ["3", "1,2,3", "4,5,6", "7,8,9"]
expected_output = "[[1, 4, 7], [2, 5, 8], [3, 6, 9]]"
"""

# Illustrative only
n = int(input())
matrix = [list(map(int, input().split(","))) for _ in range(n)]
print([list(col) for col in zip(*matrix)])
