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


class Flower(Plant):
    '''
    Class Flower defines a type of plant, which inherits features from
    class Plant, with additional feature color and bloom function.
    '''

    def __init__(self, name: str, height: int, age: int, color: str) -> None:
        '''
        Sets the name, height in cm, age in days, and color of the flower.
        '''
        super().__init__(name, height, age)
        self.color: str = color

    def bloom(self) -> str:
        '''
        Shows if the flower is blooming yet.
        '''
        if self.age >= 30:
            return f"{self.name} is blooming beautifully!"
        else:
            return f"{self.name} is not old enough to bloom."

    def __str__(self) -> str:
        '''
        Returns a string of the flower information.
        '''
        return f"{self.name} ({self.__class__.__name__}): " +\
            f"{self.height}cm, {self.age} days, {self.color} color" +\
            f"\n{self.bloom()}\n"


class Tree(Plant):
    '''
    Class Tree defines a type of plant, which inherits features from
    class Plant, with additional feature trunk_diameter and produce_shade
    function.
    '''

    def __init__(self, name: str, height: int, age: int,
                 trunk_diameter: int) -> None:
        '''
        Sets the name, height in cm, age in days, and type of the tree.
        '''
        super().__init__(name, height, age)
        self.trunk_diameter: int = trunk_diameter

    def produce_shade(self) -> int:
        '''
        Shows that the tree is producing shade.
        '''
        shade: int = int(self.trunk_diameter * 1.56)
        return shade

    def __str__(self) -> str:
        '''
        Returns a string of the tree information.
        '''
        return f"{self.name} ({self.__class__.__name__}): {self.height}cm, " +\
            f"{self.age} days, {self.trunk_diameter}cm diameter\n" +\
            f"{self.name} provides {self.produce_shade()} square meters " +\
            "of shade\n"


class Vegetable(Plant):
    '''
    Class Vegetable defines a type of plant, which inherits features from
    class Plant, with additional features harvest_season and nutritional_value.
    '''

    def __init__(self, name: str, height: int, age: int, harvest_season: str,
                 nutritoinal_value: str) -> None:
        '''
        Sets the name, height in cm, age in days, and type of the tree.
        '''
        super().__init__(name, height, age)
        self.harvest_season: str = harvest_season
        self.nutrition_value: str = nutritoinal_value

    def __str__(self) -> str:
        '''
        Returns a string of the vegetable information.
        '''
        return f"{self.name} ({self.__class__.__name__}): {self.height}cm, " +\
            f"{self.age} days, {self.harvest_season} harvest\n" +\
            f"{self.name} is rich in {self.nutrition_value}\n"


def ft_plant_types() -> None:
    '''
    Creates different types of plants and displays their information.
    No return value and no user input required.
    '''
    garden: list[Plant] = [
        Flower("Rose", 25, 30, "red"),
        Flower("Orchid", 40, 20, "purple"),
        Tree("Oak", 500, 1825, 50),
        Tree("Pine", 300, 1095, 30),
        Vegetable("Tomato", 80, 90, "summer", "vitamin C"),
        Vegetable("Potato", 60, 120, "fall", "carbohydrates")
        ]
    print("=== Garden Plant Types ===")
    for plant in garden:
        print(plant)


if __name__ == "__main__":
    ft_plant_types()
