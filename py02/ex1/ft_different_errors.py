'''
Demonstrates common errors and handles them as exceptions,
to ensure the program will not crash at runtime and print them out
to know where went wrong
'''


def garden_operations(error_type: str) -> None:
    '''
    Simulates ValueError, ZeroDivisionError, FileNotFoundError and KeyError
    situations
    '''
    if error_type == "ValueError":
        print("Testing ValueError...")
        int("abc")
    elif error_type == "ZeroDivisionError":
        print("Testing ZeroDivisionError...")
        10 / 0
    elif error_type == "FileNotFoundError":
        print("Testing FileNotFoundError...")
        open("missing.txt", "r")
    elif error_type == "KeyError":
        print("Testing KeyError...")
        d: dict[str, str] = {"plant": "rose"}
        d["missing_plant"]


def test_error_types() -> None:
    '''
    Catches errors at runtime as exceptions and prints error messages.
    Test cases are defined in garden_operations, and lastly, an additional
    case of multiple errors
    '''
    print("=== Garden Error Types Demo ===")
    print()
    error_test: list[str] = ["ValueError", "ZeroDivisionError",
                             "FileNotFoundError", "KeyError"]
    for i in error_test:
        try:
            garden_operations(i)
        except ValueError as ve:
            print(f"Caught ValueError: {ve}")
            print()
        except ZeroDivisionError as zde:
            print(f"Caught ZeroDivisionError: {zde}")
            print()
        except FileNotFoundError as fnfe:
            print(f"Caught FileNotFoundError: {fnfe}")
            print()
        except KeyError as ke:
            print(f"Caught KeyError: {ke}")
            print()
    try:
        print("Testing multiple errors together...")
        int("abc")
        10 / 0
        open("anotherone.txt", "r")
        d: dict = {}
        d["key"]
    except (ValueError, ZeroDivisionError, FileNotFoundError, KeyError):
        print("Caught an error, but program continues!")
        print()
    print("All error types tested successfully!")


if __name__ == "__main__":
    test_error_types()
