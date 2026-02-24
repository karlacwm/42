from .validator import validate_ingredients


def record_spell(spell_name: str, ingredients: str) -> str:
    validation = validate_ingredients(ingredients)
    if "INVALID" in validation:
        return f"Spell rejected: {spell_name} ({validation})"
    else:
        return f"Spell recorded: {spell_name} ({validation})"