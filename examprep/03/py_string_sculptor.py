# Assignment name  : py_string_sculptor
# Expected files   : py_string_sculptor.py
# Allowed functions: None
# --------------------------------------------------------------------------------

# Write a function that takes a string and alternates the case of its
# alphabetic characters: the first alphabetic character must be uppercase,
# the second lowercase, the third uppercase, and so on.

# Your function must be declared as follows:

# def string_sculptor(s: str) -> str:

# Rules:
# - Non-alphabetic characters (spaces, numbers, punctuation) must be left
#   exactly as they are.
# - Crucially, non-alphabetic characters DO NOT count towards the alternating
#   sequence.
# - If the string is empty, return an empty string.

# Examples:

# Input: string_sculptor("hello")
# Output: "HeLlO"

# Input: string_sculptor("hello world")
# Output: "HeLlO wOrLd"
# (Notice 'o' is Upper, the space is ignored, so 'w' becomes Lower)

# Input: string_sculptor("42 is the answer!")
# Output: "42 Is ThE aNsWeR!"

# Input: string_sculptor("   a b c d e   ")
# Output: "   A b C d E   "

def string_sculptor(s: str) -> str:
    s = s.lower()
    count = 0
    temp = []
    for char in s:
        if char.isalpha():
            count += 1
            if count % 2 != 0:
                char = char.upper()
        temp.append(char)
    s = "".join(temp)
    return s


print(string_sculptor("hello"))
print(string_sculptor("hello world"))
print(string_sculptor("42 is the answer!"))
print(string_sculptor("   a b c d e   "))
