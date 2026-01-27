class Plant:
    '''
    Class Plant defines a plant with its name, height in cm, and age in days.
    '''
    def __init__(self, name, height, age) -> None:
        self.name: str = name
        self.height: int = height
        self.age: int = age

    def grow(self, growth) -> None:
        self.height += growth
        print(f"{self.name} grew {growth}cm")

    def __str__(self) -> str:
        return f"{self.name}:


class FloweringPlant(Plant):
    def __init__(self, name, height, age, color) -> None:
        super().__init__(name, height, age)
        self.color: str = color
        self.blooming = True

    def __str__(self) -> str:
        if self.blooming == True:
            state: str = "(blooming)"
        else:
            state: str = "(not blooming)"
        return f"{self.name}: {self.height}cm, {self.color} flowers {state}"


class PrizeFlower(FloweringPlant):
    def __init__(self, name, height, color, points, age=0) -> None:
        super().__init__(name, height, color, age)
        self.points: int = points

    def __str__(self) -> str:
        plant_info: str = super().__str__()
        return f"{plant_info}, Prize points: {self.points}"
