# Assignment name  : py_brackets
# Expected files   : py_brackets.py
# Allowed functions: None
# --------------------------------------------------------------------------------

# Write a function that takes a string and checks if the brackets within it are
# properly balanced and nested.

# The function must handle three types of brackets: (), [], and {}.

# Your function must be declared as follows:

# def check_brackets(s: str) -> bool:

# Rules:
# - Every opening bracket must be closed by the corresponding closing bracket.
# - Brackets must be closed in the correct order (e.g., "([)]" is invalid).
# - If the string contains no brackets, it is considered balanced (return True)
# - Any other characters in the string should be ignored.

# Examples:

# Input: check_brackets("(hello) [world] {42}")
# Output: True

# Input: check_brackets("([)]")
# Output: False

# Input: check_brackets("{ [ ( ] ) }")
# Output: False

# Input: check_brackets("No brackets here!")
# Output: True

def check_brackets(s: str) -> bool:
    brackets = {")": "(", "]": "[", "}": "{"}
    openings = set(brackets.values())
    stack = []
    for char in s:
        if char in openings:
            stack.append(char)
        elif char in brackets:
            if not stack or stack[-1] != brackets[char]:
                return False
            stack.pop()
    return len(stack) == 0


print(check_brackets("(hello) [world] {42}"))
print(check_brackets("([)]"))
print(check_brackets("{ [ ( ] ) }"))
print(check_brackets("No brackets here!"))
