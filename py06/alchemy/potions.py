import alchemy


def healing_potion() -> str:
    fire_result = alchemy.elements.create_fire()
    water_result = alchemy.elements.create_water()
    return f"Healing potion brewed with {fire_result} and {water_result}"

def strength_potion() -> str:
    fire_result = alchemy.elements.create_fire()
    earth_result = alchemy.elements.create_earth()
    return f"Strength potion brewed with {earth_result} and {fire_result}"

def invisibility_potion() -> str:
    air_result = alchemy.elements.create_air()
    water_result = alchemy.elements.create_water()
    return f"Invisibility potion brewed with {air_result} and {water_result}"

def wisdom_potion() -> str:
    fire_result = alchemy.elements.create_fire()
    water_result = alchemy.elements.create_water()
    air_result = alchemy.elements.create_air()
    earth_result = alchemy.elements.create_earth()
    all_four_result = f"{fire_result}, {water_result}, {air_result} and {earth_result}"
    return f"Wisdom potion brewed with all elements: {all_four_result}"