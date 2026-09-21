'''
A program that reuses the Plant class from ex1 to represent any plant data,
as well simulating the growth and aging of plants.
'''


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
        self.height: int = height
        self.age_days: int = age

    def get_info(self) -> str:
        '''
        Returns a string of the plant information.
        '''
        return f"{self.name}: {self.height}cm, {self.age_days} days old"

    def grow(self) -> None:
        '''
        Increases the height of the plant, assuming a 10% growth rate.
        '''
        self.height += int(self.height * 0.1)

    def age(self) -> None:
        '''
        Increases the age of the plant by one day.
        '''
        self.age_days += 1


def ft_plant_growth() -> None:
    '''
    Simulates the growth of each plant over a week.
    Shows height and age at the start and end of the week.
    '''
    garden: list[Plant] = [
        Plant("Orchid", 40, 20),
        Plant("Rose", 25, 15),
        Plant("Tulip", 30, 10)
    ]
    print("=== Day 1 ===")
    for plant in garden:
        print(plant.get_info())
    print("=== Day 7 ===")
    for day in range(2, 8):
        for plant in garden:
            plant.age()
    for plant in garden:
        plant.grow()
        growth: int = plant.height - plant.starting_height
        print(plant.get_info())
        print(f"{plant.name}'s growth this week: +{growth}cm")


if __name__ == "__main__":
    ft_plant_growth()
