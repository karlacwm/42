'''
Demonstrates a garden management system that catches errors and problem,
such as empty plant name, water and sun level too high or too low,
and if there is enough water in tank.
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


class Plant:
    '''
    Blueprint for class Plant, including name, water level and sunlight hours.
    '''

    def __init__(self, name: str | int | None, water_level: int,
                 sunlight_hours: int) -> None:
        self.name: str | int | None = name
        self.water_level: int = water_level
        self.sunlight_hours: int = sunlight_hours


class GardenManager:
    '''
    Stores all plant data and water tank level.
    Catches errors if there is any and returns an error message.
    '''

    def __init__(self) -> None:
        '''
        Initializes a list of plants and the water tank level in the garden.
        '''
        self.garden: list[Plant] = []
        self.water_tank: int = 10

    def add_plants(self, plant: Plant) -> None:
        '''
        Adds a plant to the garden list.
        '''
        try:
            if isinstance(plant.name, int):
                raise PlantError("Plant name cannot be numbers!")
            if plant.name is None or len(plant.name) < 1:
                raise PlantError("Plant name cannot be empty!")

            if plant.water_level < 0:
                raise PlantError("Water level cannot be negative!")
            if plant.sunlight_hours < 0:
                raise PlantError("Sunlight hours cannot be negative!")
        except PlantError as e:
            print("Error adding plant:", e)
        else:
            self.garden.append(plant)
            print(f"Added {plant.name} successfully")

    def water_plants(self) -> None:
        '''
        Simulates a watering system that waters plants one by one.
        '''
        print("Opening watering system")
        try:
            for plant in self.garden:
                try:
                    if self.water_tank > 1:
                        print(f"Watering {plant.name}")
                        self.water_tank -= 1
                    else:
                        raise WaterError(
                            f"Error: Cannot water {plant.name} - empty tank!")
                except WaterError as e:
                    print(e)
                    break
        finally:
            print("Closing watering system (cleanup)")

    def check_plant_health(self) -> None:
        '''
        Checks if the parameter values are valid or out of range.
        '''
        for plant in self.garden:
            try:
                if plant.water_level > 10:
                    raise PlantError(
                        f"Water level {plant.water_level} "
                        "is too high (max 10)")
                if plant.water_level < 1:
                    raise PlantError(
                        f"Water level {plant.water_level} is too low (min 1)")
                if plant.sunlight_hours > 12:
                    raise PlantError(
                        f"Sunlight hours {plant.sunlight_hours} "
                        "is too high (max 12)")
                if plant.sunlight_hours < 2:
                    raise PlantError(
                        f"Sunlight hours {plant.sunlight_hours} "
                        "is too low (min 2)")
            except PlantError as e:
                print(f"Error checking {plant.name}:", e)
            else:
                print(f"{plant.name}: healthy (water: {plant.water_level},",
                      f"sun: {plant.sunlight_hours})")

    def watering(self) -> None:
        '''
        Raises a WaterError when the tank level is lower than 3.
        '''
        if self.water_tank < 3:
            raise WaterError("Not enough water in the tank!")

    def error_recovery(self) -> None:
        '''
        Shows the system continues working after errors
        '''
        try:
            self.watering()
        except GardenError as e:
            print("Caught GardenError:", e)
        finally:
            print("System recovered and continuing...")


def test_garden_management() -> None:
    '''
    Testing all functions in class GardenManager with valid and invalid values.
    '''
    manager = GardenManager()
    garden: list[Plant] = [
        Plant("tomato", 5, 8),
        Plant("lettuce", 15, 5),
        Plant(None, 5, 5),
        Plant(22, 5, 5)
    ]
    print("=== Garden Management System ===", end="\n\n")
    print("Adding plants to garden...")
    for plant in garden:
        manager.add_plants(plant)
    print()
    print("Watering plants...")
    manager.water_plants()
    print()
    print("Checking plant health...")
    manager.check_plant_health()
    print()
    print("Testing error recovery...")
    manager.water_tank = 0
    manager.error_recovery()
    print()
    print("Garden management system test complete!")


if __name__ == "__main__":
    test_garden_management()
