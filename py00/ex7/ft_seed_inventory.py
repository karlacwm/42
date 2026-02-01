def ft_seed_inventory(seed_type: str, quantity: int, unit: str) -> None:
    seed_name: str = seed_type.capitalize()
    if unit == "packets":
        print(seed_name, "seeds:", quantity, unit, "available")
    elif unit == "grams":
        print(seed_name, "seeds:", quantity, unit, "total")
    elif unit == "area":
        print(seed_name, "seeds:", "covers", quantity, "square meters")
    else:
        print("Unknown unit type")
