# py_number_base_converter
# py_number_base_converter.py
# ✕
# Assignment
# Write a function that converts a number from one base to another.
# Support bases from 2 to 36 inclusive, using digits 0-9 and letters A-Z for values 10-35. Return "ERROR" for invalid inputs (base, digits)
# Function signature
# def number_base_converter(number: str, from_base: int, to_base: int) -> str:
# Examples
# Input
# number_base_converter("1010", 2, 10)
# Output
# "10"
# Input
# number_base_converter("FF", 16, 10)
# Output
# "255"
# Input
# number_base_converter("255", 10, 16)
# Output
# "FF"
# Input
# number_base_converter("123", 10, 2)
# Output
# "1111011"
# Input
# number_base_converter("Z", 36, 10)
# Output
# "35"
# Input
# number_base_converter("35", 10, 36)
# Output
# "Z"
# Input
# number_base_converter("123", 1, 10)
# Output
# "ERROR"
# Input
# number_base_converter("G", 16, 10)
# Output
# "ERROR"
# ==========================================

def number_base_converter(number: str, from_base: int, to_base: int) -> str:
    if not (2 <= from_base <= 36 and 2 <= to_base <= 36):
        return "ERROR"

    try:
        base_10 = int(number, from_base)
    
        base = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        if base_10 == 0:
            return "0"
        
        result = ""

        while base_10 > 0:
            pos = base_10 % to_base
            base_10 = base_10 // to_base
            result = base[pos] + result
        return result

    except ValueError:
        return "ERROR"


print(number_base_converter("1010", 2, 10))
print(number_base_converter("FF", 16, 10))
print(number_base_converter("255", 10, 16))
print(number_base_converter("123", 10, 2))
print(number_base_converter("Z", 36, 10))
print(number_base_converter("35", 10, 36))
print(number_base_converter("123", 1, 10))
print(number_base_converter("G", 16, 10))