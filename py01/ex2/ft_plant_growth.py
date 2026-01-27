class Plant:
    '''
    Class Plant defines a plant with its name, height in cm, and age in days.
    '''

    def __init__(self, name: str, height_cm: int, age_days: int) -> None:
        '''
        Sets the name, height in cm, and age in days of the plant.
        '''
        self.name: str = name
        self.height_cm: int = height_cm
        self.age_days: int = age_days

    def get_info(self) -> str:
        '''
        Returns a string of the plant information.
        '''
        return f"{self.name}: {self.height_cm}cm, {self.age_days} days old"

    def grow(self) -> int:
        '''
        Finds how much the plant grows, assuming a 10% growth rate.
        '''
        return int(self.height_cm * 0.1)

    def age(self) -> None:
        '''
        Increases the age of the plant by one day.
        '''
        self.age_days += 1


def ft_plant_growth() -> None:
    '''
    Simulates the growth of each plant over a week.
    No return value and no user input required.
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
        growth: int = plant.grow()
        plant.height_cm += growth
        print(plant.get_info())
        print(f"{plant.name}'s growth this week: +{growth}cm")


if __name__ == "__main__":
    ft_plant_growth()
