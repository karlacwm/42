class Plant:
    '''
    Class Plant defines a plant with its name, height in cm, and age in days.
    '''

    def __init__(self, name: str, height: int, age: int) -> None:
        '''
        Sets the name, height in cm, and age in days of the plant.
        '''
        self.name: str = name
        self.starting_height: int = height
        self.starting_age: int = age


def ft_plant_factory() -> None:
    '''
    Creates plants with initial values and add to a garden list.
    Counts total plants created.
    '''
    garden: list[Plant] = [
        Plant("Orchid", 40, 20),
        Plant("Rose", 20, 10),
        Plant("Tulip", 35, 15),
        Plant("Cactus", 10, 35),
        Plant("Sunflower", 50, 22)
    ]
    print("=== Plant Factory Output ===")
    for plant in garden:
        print(
            f"Created: {plant.name} "
            f"({plant.starting_height}cm, {plant.starting_age} days)"
        )
    print("\nTotal plants created:", len(garden))


if __name__ == "__main__":
    ft_plant_factory()
