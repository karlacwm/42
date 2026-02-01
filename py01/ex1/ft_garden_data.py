'''
A program that organises information with a Plant class,
which serves as a blue print to represent any plant.
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
        self.height: int = height
        self.age: int = age

    def __str__(self) -> str:
        '''
        Returns a string of the plant information.
        '''
        return f"{self.name}: {self.height}cm, {self.age} days old"


def ft_garden_data() -> None:
    '''
    Displays plants information in an organized way,
    including their name, height, and age.
    '''
    garden: list[Plant] = [
        Plant("Orchid", 40, 20),
        Plant("Rose", 25, 15),
        Plant("Tulip", 20, 10)
    ]
    print("=== Garden Plant Registry ===")
    for plant in garden:
        print(plant)


if __name__ == "__main__":
    ft_garden_data()
