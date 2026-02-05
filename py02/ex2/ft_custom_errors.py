'''
Creates my own error types for my garden program,
including GardenError, PlantError and WaterError,
and demonstrates them in different situations.
'''


class GardenError(Exception):
    '''
    A basic error for garden problems.
    '''
    pass


class PlantError(GardenError):
    '''
    For problems with plants (inherits from GardenError).
    '''
    pass


class WaterError(GardenError):
    '''
    For problems with watering (inherits from GardenError).
    '''
    pass


def wilting(plant_name: str, wilting: bool) -> None:
    '''
    Raises a PlantError when the condition wilting is true.
    '''
    if wilting:
        raise PlantError(f"The {plant_name} plant is wilting!")


def watering(tank_level: int) -> None:
    '''
    Raises a WaterError when the tank level is lower than 3.
    '''
    if tank_level < 2:
        raise WaterError("Not enough water in the tank!")


def garden_error_types() -> None:
    '''
    Shows that my own error types catches the errors
    when there is problem with wilting and watering,
    and GardenError catches all garden-related errors.
    '''
    print("=== Custom Garden Errors Demo ===", end="\n\n")
    print("Testing PlantError...")
    try:
        wilting("tomato", True)
    except PlantError as e:
        print("Caught PlantError:", e, end="\n\n")
    print("Testing WaterError...")
    try:
        watering(1)
    except WaterError as e:
        print("Caught WaterError:", e, end="\n\n")
    print("Testing catching all garden errors...")
    try:
        wilting("tomato", True)
    except GardenError as e:
        print("Caught a garden error:", e)
    try:
        watering(1)
    except GardenError as e:
        print("Caught a garden error:", e)
    print("\nAll custom error types work correctly!")


if __name__ == "__main__":
    garden_error_types()
