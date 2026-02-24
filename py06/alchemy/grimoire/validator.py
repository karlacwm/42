def validate_ingredients(ingredients: str) -> str:
    valid_ingredients = {"fire", "water", "earth", "air"}
    if any(i in ingredients for i in valid_ingredients):
        return f"{ingredients} - VALID" 
    return f"{ingredients} - INVALID"