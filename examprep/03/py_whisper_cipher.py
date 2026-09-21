# Assignment name  : py_whisper_cipher
# Expected files   : py_whisper_cipher.py
# Allowed functions: None
# --------------------------------------------------------------------------------

# Write a function that takes a string `s` and an integer `shift`. It must
# return a new string where every alphabetic character is shifted by the
# `shift` amount.

# Your function must be declared as follows:

# def whisper_cipher(s: str, shift: int) -> str:

# Rules:
# - The shift must wrap around the alphabet (e.g., shifting 'z' by 1 results
#   in 'a').
# - The shift can be a very large positive number (e.g., shift=100).
# - You must preserve the original case of the letters (uppercase stays
#   uppercase, lowercase stays lowercase).
# - Any non-alphabetic characters (spaces, punctuation, numbers) should remain
#   unchanged.
# - If the string is empty, return an empty string.

# Examples:

# Input: whisper_cipher("abc", 1)
# Output: "bcd"

# Input: whisper_cipher("Zeta 42!", 2)
# Output: "Bgvc 42!"

# Input: whisper_cipher("Hello World", 42)
# Output: "Xubbe Mehbt"

def whisper_cipher(s: str, shift: int) -> str:
    lower = "abcdefghijklmnopqrstuvwxyz"
    upper = lower.upper()
    temp = []
    while shift >= 26:
        shift = shift % 26
    for char in s:
        if char.isupper():
            temp.append(upper[(ord(char) - ord("A") + shift) % 26])
        elif char.islower():
            temp.append(lower[(ord(char) - ord("a") + shift) % 26])
        else:
            temp.append(char)
    s = "".join(temp)
    return s


print(whisper_cipher("abc", 1))
print(whisper_cipher("Zeta 42!", 2))
print(whisper_cipher("Hello World", 42))
