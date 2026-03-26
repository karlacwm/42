# Assignment name  : py_pattern_tracker
# Expected files   : py_pattern_tracker.py
# Allowed functions: None
# --------------------------------------------------------------------------------

# Write a function that takes a `pattern` string and a string `s` of words
# separated by spaces. The function must return True if `s` follows the exact
# same pattern.

# "Following the pattern" means there is a full bijection (a two-way match)
# between a letter in `pattern` and a non-empty word in `s`.

# Your function must be declared as follows:

# def pattern_tracker(pattern: str, s: str) -> bool:

# Rules:
# - You must map each character in `pattern` to exactly one unique word in `s`.
# - No two characters can map to the same word.
# - If the number of characters in `pattern` does not match the number of words
#   in `s`, return False.

# Examples:

# Input: pattern_tracker("abba", "dog cat cat dog")
# Output: True
# (Explanation: 'a' maps to "dog", 'b' maps to "cat")

# Input: pattern_tracker("abba", "dog cat cat fish")
# Output: False
# (Explanation: 'a' maps to "dog", but then 'a' tries to map to "fish" at the
# end)

# Input: pattern_tracker("aaaa", "dog cat cat dog")
# Output: False

# Input: pattern_tracker("abba", "dog dog dog dog")
# Output: False
# (Explanation: 'a' and 'b' cannot both map to "dog")


print()
