# Assignment name  : is_palindrome
# Expected files   : is_palindrome.py
# Allowed functions: None
# --------------------------------------------------------------------------------

# Write a function that checks if a given string is a palindrome. A string is a
# palindrome if it reads the same forwards and backwards.

# Your function must be declared as follows:

# def is_palindrome(s: str) -> bool:

# Rules:
# - You must ignore all non-alphanumeric characters (spaces, punctuation, etc.)
# - The check must be case-insensitive (treat 'A' and 'a' as the same).
# - An empty string or a string with no alphanumeric characters is considered a
#   palindrome (return True).

# Examples:

# Input: is_palindrome("A man, a plan, a canal: Panama")
# Output: True

# Input: is_palindrome("race a car")
# Output: False

# Input: is_palindrome(" ")
# Output: True

# Input: is_palindrome("No lemon, no melon!")
# Output: True

def is_palindrome(s: str) -> bool:
    word = []
    for char in s.lower():
        if char.isalnum():
            word.append(char)
    "".join(word)
    if word[::1] != word[::-1]:
        return False
    return True


print(is_palindrome("A man, a plan, a canal: Panama"))
print(is_palindrome("race a car"))
print(is_palindrome(" "))
print(is_palindrome("No lemon, no melon!"))
