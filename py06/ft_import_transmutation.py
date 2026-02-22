import alchemy.elements
from alchemy.elements import create_water
from alchemy.potions import healing_potion as heal
from alchemy.elements import create_fire, create_earth
from alchemy.potions import strength_potion


def ft_import_transmutation() -> None:
    print("=== Import Transmutation Mastery ===")
    print()
    print("Method 1 - Full module import:")
    fire = alchemy.elements.create_fire()
    print("alchemy.elements.create_fire():", fire)
    print()
    print("Method 2 - Specific function import:")
    water = create_water()
    print("create_water():", water)
    print()
    print("Method 3 - Aliased import:")
    healing = heal()
    print("heal():", healing)
    print()
    print("Method 4 - Multiple imports:")
    earth = create_earth()
    fire = create_fire()
    strength = strength_potion()
    print("create_earth():", earth)
    print("create_fire():", fire)
    print("strength_potion():", strength)
    print()
    print("All import transmutation methods mastered!")


if __name__== "__main__":
    ft_import_transmutation()