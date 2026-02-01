'''
The program handles garden data like a manager.
For each garden, the program creates a garden report on the owner,
his or her plants, the type of plants owned, the growing status of the plants,
and lastly the score of the garden based on a prize-points collecting system.
There is a validation for plant height to track if the data is valid.
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

    def grow(self) -> int:
        '''
        Increases the height of the plant by growth cm,
        which is passed as parameter,
        assuming consistency of 5% growth for this simulation.
        '''
        old_height: int = self.height
        self.height += int(self.height * 0.05)
        growth: int = self.height - old_height
        print(f"{self.name} grew {growth}cm")
        return growth

    def __str__(self) -> str:
        '''
        Returns a string of the plant information.
        '''
        return f"{self.name}: {self.height}cm"


class FloweringPlant(Plant):
    '''
    Class FloweringPlant defines a flowering plant,
    which inherits features from class Plant, with additional feature color.
    '''

    def __init__(self, name: str, height: int, age: int, color: str) -> None:
        '''
        Sets the name, height in cm, age in days,
        and color of the flowering plant.
        '''
        super().__init__(name, height, age)
        self.color: str = color
        self.blooming = True

    def __str__(self) -> str:
        '''
        Returns a string of the flowering plant information,
        and whether it is blooming.
        '''
        if self.age > 30:
            state: str = "(blooming)"
        else:
            state = "(not yet blooming)"
        return f"{self.name}: {self.height}cm, {self.color} flowers {state}"


class PrizeFlower(FloweringPlant):
    '''
    Class PrizeFlower defines a flower that counts to prize points,
    which inherits features from class FloweringPlant,
    with additional feature points.
    '''

    def __init__(self, name: str, height: int, age: int, color: str,
                 points: int) -> None:
        '''
        Sets the name, height in cm, age in days, color,
        and prize points of the prize flower.
        '''
        super().__init__(name, height, age, color)
        self.points: int = points

    def __str__(self) -> str:
        '''
        Returns a string of the prize flower information,
        including prize points.
        '''
        plant_info: str = super().__str__()
        return f"{plant_info}, Prize points: {self.points}"


class GardenManager:
    '''
    Class GardenManager manages information of multiple gardens.
    '''
    total_gardens: int = 0

    def __init__(self, owner: str) -> None:
        '''
        Sets the owner of the garden manager
        and initializes an empty garden list.
        '''
        self.owner: str = owner
        self.garden_list: list[Plant] = []
        self.total_growth: int = 0
        GardenManager.total_gardens += 1

    def add_plant(self, plant: Plant) -> None:
        '''
        Adds a plant to the garden list.
        '''
        self.garden_list.append(plant)
        print(f"Added {plant.name} to {self.owner}'s garden.")

    def grow_plant(self) -> None:
        '''
        Shows the garden owner who is helping all plants grow,
        and updates the total growth for garden report statistics.
        '''
        print(f"{self.owner} is helping all plants grow...")
        for plant in self.garden_list:
            growth: int = plant.grow()
            self.total_growth += growth

    class GardenStats:
        '''
        Class GardenStats is nested inside class GardenManager,
        which helps to calculates scores and validate data.
        '''
        @staticmethod
        def validate_height(height: int) -> bool:
            '''
            Validates if the height of a plant is non-negative.
            '''
            return height >= 0

        @staticmethod
        def garden_score(garden: list[Plant]) -> int:
            '''
            Calculates the garden score
            based on the heights of plants and prize points.
            '''
            score: int = 0
            for plant in garden:
                score += plant.height
                if isinstance(plant, PrizeFlower):
                    score += plant.points
            return score

    @classmethod
    def create_garden_network(cls, owner: str) -> 'GardenManager':
        '''
        Creates a garden manager using class type GardenManager.
        '''
        return cls(owner)

    def garden_report(self) -> int:
        '''
        Generates a report of the garden, including owner, plant details,
        garden statistics, height validation, and returns the garden score.
        '''
        print(f"=== {self.owner}'s Garden Report ===")
        print("Plants in garden:")
        regular: int = 0
        flowering: int = 0
        prize: int = 0
        for plant in self.garden_list:
            print(f"- {plant}")
            if isinstance(plant, PrizeFlower):
                prize += 1
            elif isinstance(plant, FloweringPlant):
                flowering += 1
            else:
                regular += 1
        print(
            f"\nPlants added: {len(self.garden_list)}, "
            f"Total growth: {self.total_growth}cm"
        )
        print(
            f"Plant types: {regular} regular, {flowering} flowering,"
            f" {prize} prize flowers"
        )
        valid_all: bool = all(self.GardenStats.validate_height(plant.height)
                              for plant in self.garden_list)
        print(f"\nHeight validation test: {valid_all}")
        return GardenManager.GardenStats.garden_score(self.garden_list)


def ft_garden_analytics() -> None:
    '''
    Demonstrates the Garden Management System by creating gardens,
    adding plants, growing them, and generating reports.
    '''
    print("=== Garden Management System Demo ===")
    alice: GardenManager = GardenManager.create_garden_network("Alice")
    bob: GardenManager = GardenManager.create_garden_network("Bob")
    alice.add_plant(Plant("Oak Tree", 100, 10))
    alice.add_plant(FloweringPlant("Rose", 25, 35, "red"))
    alice.add_plant(PrizeFlower("Sunflower", 50, 25, "yellow", 10))
    bob.add_plant(Plant("Pine Tree", 70, 40))
    bob.add_plant(PrizeFlower("Orchid", 45, 30, "purple", 30))
    bob.add_plant(PrizeFlower("Lily", 50, 50, "white", 30))
    bob.add_plant(PrizeFlower("Sunflower", 20, 10, "yellow", 10))
    print("")
    alice.grow_plant()
    print("")
    bob.grow_plant()
    print("")
    alice_score: int = alice.garden_report()
    print("")
    bob_score: int = bob.garden_report()

    print(
        f"Garden scores - {alice.owner}: {alice_score}"
        f", {bob.owner}: {bob_score}"
    )
    print(f"Total gardens managed: {GardenManager.total_gardens}")


if __name__ == "__main__":
    ft_garden_analytics()
