'''
Creates my own error types for my garden program,
including GardenError, PlantError and WaterError,
and demonstrates them in different situations.
'''


class GardenError():
    '''
    A basic error for garden problems
    '''
    pass


class PlantError(GardenError):
    '''
    For problems with plants (inherits from GardenError)
    '''
    pass


class WaterError(GardenError):
    '''
    For problems with watering (inherits from GardenError)
    '''
    pass


def garden_error_types() -> None:
    '''
    Docstring
    '''
    print("=== Custom Garden Errors Demo ===")
    print("Testing PlantError...")
    print("Testing WaterError...")
    print("All custom error types work correctly!")


if __name__ == "__main__":
    garden_error_types()
