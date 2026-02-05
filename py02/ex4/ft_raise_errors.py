'''
Demonstrates how to detect problem and raise errors in the program,
returns an error message to signal something is wrong and
a success message if everything is good.
'''


def check_plant_health(plant_name: str | None, water_level: int,
                       sunlight_hours: int) -> None:
    '''
    Checks if the parameter values are valid or out of range.
    '''
    try:
        if plant_name is None:
            raise ValueError("Plant name cannot be empty!")
        if water_level > 10:
            raise ValueError(f"Water level {water_level} is too high (max 10)")
        if water_level < 1:
            raise ValueError(f"Water level {water_level} is too low (min 1)")
        if sunlight_hours > 12:
            raise ValueError(
                f"Sunlight hours {sunlight_hours} is too high (max 12)")
        if sunlight_hours < 2:
            raise ValueError(
                f"Sunlight hours {sunlight_hours} is too low (min 2)")
    except ValueError as e:
        print("Error:", e)
    else:
        print(f"Plant '{plant_name}' is healthy!")


def test_plant_checks() -> None:
    '''
    Shows a few test cases to test if the check_plant_health catches errors,
    and returns a helpful message.
    '''
    print("=== Garden Plant Health Checker ===")
    print()
    print("Testing good values...")
    check_plant_health("tomato", 5, 5)
    print()
    print("Testing empty plant name...")
    check_plant_health(None, 5, 5)
    print()
    print("Testing bad water level...")
    check_plant_health("tomato", 20, 5)
    print()
    print("Testing bad sunlight hours...")
    check_plant_health("tomato", 5, 0)
    print()
    print("All error raising tests completed!")


if __name__ == "__main__":
    test_plant_checks()
