# method 1
import alchemy.elements
# method 2
from alchemy.elements import create_water
# method 3
from alchemy.potions import healing_potion as heal
# method 4
from alchemy.elements import create_fire, create_earth
from alchemy.potions import strength_potion


def method_1() -> None:
    print("Method 1 - Full module import:")
    fire: str = alchemy.elements.create_fire()
    print("alchemy.elements.create_fire():", fire)
    print()


def method_2() -> None:
    print("Method 2 - Specific function import:")
    water: str = create_water()
    print("create_water():", water)
    print()


def method_3() -> None:
    print("Method 3 - Aliased import:")
    healing: str = heal()
    print("heal():", healing)
    print()


def method_4() -> None:
    print("Method 4 - Multiple imports:")
    earth: str = create_earth()
    fire: str = create_fire()
    strength: str = strength_potion()
    print("create_earth():", earth)
    print("create_fire():", fire)
    print("strength_potion():", strength)
    print()


def ft_import_transmutation() -> None:
    print("=== Import Transmutation Mastery ===")
    print()
    method_1()
    method_2()
    method_3()
    method_4()
    print("All import transmutation methods mastered!")


if __name__ == "__main__":
    ft_import_transmutation()
