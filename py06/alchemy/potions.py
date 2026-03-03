from alchemy.elements import (create_fire, create_water,
                              create_air, create_earth)


def healing_potion() -> str:
    return f"Healing potion brewed with {create_fire()} and {create_water()}"


def strength_potion() -> str:
    return f"Strength potion brewed with {create_earth()} and {create_fire()}"


def invisibility_potion() -> str:
    return (f"Invisibility potion brewed with {create_air()} "
            f"and {create_water()}")


def wisdom_potion() -> str:
    all_four: str = (f"{create_fire()}, {create_water()}, {create_air()} "
                     f"and {create_earth()}")
    return f"Wisdom potion brewed with all elements: {all_four}"
