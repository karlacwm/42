'''
Two methods are used to check if the temperature value is valid,
and to handle error cases when it is invalid, to make sure the program
does not crash.
'''


def check_temperature(temp_str: str) -> int:
    '''
    Validates temperature input (integers and 0-40) and
    returns the temperature as integer if it passes the checks.
    '''
    try:
        temperature: int = int(temp_str)
    except ValueError:
        raise ValueError(f"Error: '{temp_str}' is not a valid number")
    if temperature > 40:
        raise ValueError(
            f"Error: {temperature}°C is too hot for plants (max 40°C)")
    if temperature < 0:
        raise ValueError(
            f"Error: {temperature}°C is too cold for plants (min 0°C)")
    return temperature


def test_temperature_input() -> None:
    '''
    Functions as a checker to take in input value for checking.
    Checks the input with check_temperature method.
    '''
    print("=== Garden Temperature Checker ===", end="\n\n")
    temp_test: list[str] = ["25", "abc", "100", "-50"]
    for i in temp_test:
        print(f"Testing temperature: {i}")
        try:
            checked: int = check_temperature(i)
            print(f"Temperature {checked}°C is perfect for plants!")
        except ValueError as ve:
            print(ve)
        print()
    print("All tests completed - program didn't crash!")


if __name__ == "__main__":
    test_temperature_input()
