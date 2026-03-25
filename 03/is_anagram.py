# Assignment name  : is_anagram
# Expected files   : is_anagram.py
# Allowed functions: None
# --------------------------------------------------------------------------------

# Write a function that takes two strings, `s` and `t`, and returns True if
# `t` is an anagram of `s`, and False otherwise.

# An Anagram is a word or phrase formed by rearranging the letters of a
# different word or phrase, typically using all the original letters exactly
# once.

# Your function must be declared as follows:

# def is_anagram(s: str, t: str) -> bool:

# Rules:
# - The comparison is case-sensitive ('a' is not the same as 'A').
# - You do not need to ignore spaces or punctuation (treat them as normal
#   characters).
# - If the strings have different lengths, they cannot be anagrams.

# Examples:

# Input: is_anagram("anagram", "nagaram")
# Output: True

# Input: is_anagram("rat", "car")
# Output: False

# Input: is_anagram("listen", "silent")
# Output: True

# Input: is_anagram("hello", "helo")
# Output: False

def is_anagram(s: str, t: str) -> bool:
    char_set = []
    if len(s) is not len(t):
        return False
    for char in s:
        char_set.append(char)
    for char in t:
        if char in char_set:
            char_set.remove(char)
        elif char not in char_set:
            return False
        elif not char_set:
            return False
    return True

# smart one-line solution
# # ====================================
# def is_anagram(s: str, t: str) -> bool:
#     return sorted(s) == sorted(t)


print(is_anagram("anagram", "nagaram"))
print(is_anagram("rat", "car"))
print(is_anagram("listen", "silent"))
print(is_anagram("hello", "helo"))
