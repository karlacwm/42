# Assignment name  : py_atoi_base
# Expected files   : py_atoi_base.py
# Allowed functions: None
# --------------------------------------------------------------------------------

# Write a function that converts a string argument `s` (representing a number
# in a given `base`) into an integer.

# Your function must be declared as follows:

# def atoi_base(s: str, base: int) -> int:

# Rules:
# - `base` will be an integer from 2 to 16. If `base` is outside this range,
#   return 0.
# - The string `s` may contain leading whitespaces.
# - The string `s` may be preceded by a single '+' or '-' sign.
# - Characters representing digits above 9 are 'a' to 'f' (or 'A' to 'F'). Your
#   function must handle both uppercase and lowercase letters.
# - If the string contains any character that is invalid for the given base
#   (e.g., '3' in base 2, or 'g' in base 16), stop reading and return the
#   accumulated integer up to that point.
# - If the string is empty or has no valid digits to start with, return 0.

# Examples:

# Input: atoi_base("101", 2)
# Output: 5

# Input: atoi_base("   -1A3", 16)
# Output: -419

# Input: atoi_base("123", 10)
# Output: 123

# Input: atoi_base("42xyz", 10)
# Output: 42

# Input: atoi_base("  +ff", 16)
# Output: 255


# USING int()
# ========================================
# def atoi_base(s: str, base: int) -> int:
#     if base != 2 or base != 10 or base != 16:
#         return 0
#     base_char = "+- 0123456789abcdefABCDEF"
#     stack = []
#     for char in s:
#         if char in base_char:
#             stack.append(char)
#         elif not stack:
#             return 0
#     num = "".join(stack)
#     result = int(num, base)
#     return result


def atoi_base(s: str, base: int) -> int:
    if base < 2 or base > 16:
        return 0

    i = 0
    n = len(s)

    while i < n and s[i].isspace():
        i += 1

    sign = 1
    if i < n and s[i] in "+-":
        if s[i] == "-":
            sign = -1
        i += 1

    def char_to_val(char: str) -> int:
        if "0" <= char <= "9":
            return ord(char) - ord("0")
        if "a" <= char <= "f":
            return ord(char) - ord("a") + 10
        if "A" <= char <= "F":
            return ord(char) - ord("A") + 10
        return -1

    value = 0
    has_digit = False

    while i < n:
        digit = char_to_val(s[i])
        if digit < 0 or digit >= base:
            break
        value = value * base + digit
        has_digit = True
        i += 1

    if not has_digit:
        return 0

    return sign * value


print(atoi_base("101", 2))
print(atoi_base("   -1A3", 16))
print(atoi_base("123", 10))
print(atoi_base("42xyz", 10))
print(atoi_base("  +ff", 16))
