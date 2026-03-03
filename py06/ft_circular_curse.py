from alchemy.grimoire import validate_ingredients, record_spell


def ingredient_validation() -> None:
    print("Testing ingredient validation:")
    print("validate_ingredients(\"fire air\"): "
          f"{validate_ingredients('fire air')}")
    print(f"validate_ingredients(\"dragon scales\"): "
          f"{validate_ingredients('dragon scales')}")
    print()


def spell_recording() -> None:
    print("Testing spell recording with validation:")
    print(f"record_spell(\"Fireball\", \"fire air\"): "
          f"{record_spell('Fireball', 'fire air')}")
    print(f"record_spell(\"Dark Magic\", \"shadow\"): "
          f"{record_spell('Dark Magic', 'shadow')}")
    print()


# delay import in spellbook.py
def late_imports() -> None:
    print("Testing late import technique:")
    print("record_spell(\"Lightning\", \"air\"): "
          f"{record_spell('Lightning', 'air')}")
    print()


# pass validate_ingredients as a function parameter in spellbook.py
# def dependency_injection() -> None:
#     print("Testing late import technique:")
#     print("record_spell(\"Lightning\", \"air\"): "
#           f"{record_spell('Lightning', 'air', validate_ingredients)}")
#     print()


def ft_circular_curse() -> None:
    print("=== Circular Curse Breaking ===")
    print()
    ingredient_validation()
    spell_recording()
    late_imports()
    # dependency_injection()
    print("Circular dependency curse avoided using late imports!")
    print("All spells processed safely!")


if __name__ == "__main__":
    ft_circular_curse()
