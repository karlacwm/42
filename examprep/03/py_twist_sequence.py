
# py_twist_sequence
# py_twist_sequence.py
# ✕
# Assignment
# Write a function that rotates an array to the right by k positions, rotating right by k means the last k elements move to the front.
# Function signature
# def twist_sequence(arr: list[int], k: int) -> list[int]:
# Examples
# Input
# twist_sequence([1, 2, 3, 4, 5], 2)
# Output
# [4, 5, 1, 2, 3]
# Input
# twist_sequence([1, 2, 3], 1)
# Output
# [3, 1, 2]
# Input
# twist_sequence([1, 2, 3, 4], 0)
# Output
# [1, 2, 3, 4]
# Input
# twist_sequence([1, 2, 3], 5)
# Output
# [2, 3, 1]
# Input
# twist_sequence([], 3)
# Output
# []
# =========================================

def twist_sequence(arr: list[int], k: int) -> list[int]:
    if k == 0 or not arr:
        return arr
    last = len(arr) - 1
    while k > 0:
        arr.insert(0, arr[last])
        arr.pop()
        k = k - 1
    return arr


print(twist_sequence([1, 2, 3, 4, 5], 2))
print(twist_sequence([1, 2, 3], 1))
print(twist_sequence([1, 2, 3, 4], 0))
print(twist_sequence([1, 2, 3], 5))
print(twist_sequence([], 3))
