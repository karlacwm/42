def ingredient_validation() -> None:
    from alchemy.grimoire.validator import validate_ingredients
    print("Testing ingredient validation:")
    print(f"validate_ingredients(\"fire air\"): {validate_ingredients('fire air')}")
    print(f"validate_ingredients(\"dragon scales\"): {validate_ingredients('dragon scales')}")
    print()


def spell_recording() -> None:
    from alchemy.grimoire.spellbook import record_spell
    print("Testing spell recording with validation:")
    print(f"record_spell(\"Fireball\", \"fire air\"): {record_spell("Fireball", "fire air")}")
    print(f"record_spell(\"Dark Magic\", \"shadow\"): {record_spell("Dark Magic", "shadow")}")
    print()


def ft_circular_curse() -> None:
    print("=== Circular Curse Breaking ===")
    print()
    ingredient_validation()
    spell_recording()
    print("Circular dependency curse avoided using late imports!")
    print("All spells processed safely!")


if __name__ == "__main__":
    ft_circular_curse()