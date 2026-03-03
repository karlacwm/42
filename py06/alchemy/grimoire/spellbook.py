def record_spell(spell_name: str, ingredients: str) -> str:
    from alchemy.grimoire import validate_ingredients
    validation: str = validate_ingredients(ingredients)
    if "INVALID" in validation:
        return f"Spell rejected: {spell_name} ({validation})"
    else:
        return f"Spell recorded: {spell_name} ({validation})"

# dependency injection, without importing
# import typing for type hints only
# from typing import Callable


# def record_spell(spell_name: str, ingredients: str,
#                  validate_ingredients: Callable[[str], str]) -> str:
#     validation: str = validate_ingredients(ingredients)
#     if "INVALID" in validation:
#         return f"Spell rejected: {spell_name} ({validation})"
#     else:
#         return f"Spell recorded: {spell_name} ({validation})"
