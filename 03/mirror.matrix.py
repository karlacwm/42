# Assignment name  : mirror_matrix_py
# Expected files   : mirror_matrix.py
# Allowed functions: None
# --------------------------------------------------------------------------------

# Write a function that takes a 2D array of integers (a matrix) and returns a
# new matrix that is mirrored horizontally. This means the order of elements
# inside each row should be reversed.

# Your function must be declared as follows:

# def mirror_matrix(matrix: list[list[int]]) -> list[list[int]]:

# Rules:
# - The function should handle empty matrices (e.g., [] or [[]]).
# - The original matrix should not be modified (return a new one).
# - You can assume all rows in a non-empty matrix will have the same length.

# Examples:

# Input:
# [
#   [1, 2, 3],
#   [4, 5, 6],
#   [7, 8, 9]
# ]
# Output:
# [
#   [3, 2, 1],
#   [6, 5, 4],
#   [9, 8, 7]
# ]

# Input: mirror_matrix([[42]])
# Output: [[42]]

# Input: mirror_matrix([])
# Output: []

# NOT SOLUTION
# ========================================
# def mirror_matrix(matrix: list[list[int]]) -> list[list[int]]:
#     mirrored_list: list[list[int]] = []
#     num_set = []
#     for num_set in matrix:
#         num_set.reverse()
#         mirrored_list.append(num_set)
#     return mirrored_list


def mirror_matrix(matrix: list[list[int]]) -> list[list[int]]:
    return [row[::-1] for row in matrix]
# slicing: [start : stop : step]


print(mirror_matrix([[1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9]]))
print(mirror_matrix([[42]]))
print(mirror_matrix([]))
