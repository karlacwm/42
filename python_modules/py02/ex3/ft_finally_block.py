'''
Demonstrates the use of finally block to run as cleanup,
whether there was an error or not at runtime.
'''


def water_plants(plant_list: list[str | int | None]) -> None:
    '''
    Simulates a watering system that waters plants one by one.
    '''
    print("Opening watering system")
    try:
        for plant in plant_list:
            try:
                if isinstance(plant, str) and len(plant) > 0:
                    print(f"Watering {plant}")
                else:
                    raise Exception(
                        f"Error: Cannot water {plant} - invalid plant!")
            except Exception as e:
                print(e)
    finally:
        print("Closing watering system (cleanup)")


def test_watering_system() -> None:
    '''
    Demonstrates two test cases when the watering system runs fully,
    and when it fails to run till the end, either case there is a finally
    block at the end as cleanup.
    '''
    print("=== Garden Watering System ===", end="\n\n")
    plant_list: list[str | int | None] = ["tomato", "lettuce", "carrots"]
    plant_list_error: list[str | int | None] = ["tomato", None, 12, ""]
    print("Testing normal watering...")
    water_plants(plant_list)
    print("Watering completed successfully!", end="\n\n")
    print("Testing with error...")
    water_plants(plant_list_error)
    print()
    print("Cleaning always happens, even with errors!")


if __name__ == "__main__":
    test_watering_system()
