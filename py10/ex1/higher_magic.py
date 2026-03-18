from typing import Callable, Any


# * and ** are unpacking operators when not used in math
# * for lists and tuples, ** for dicts
# *args and **kwargs: dont know how many arguments, but just catch them all
# *args (arguments): catches any arguments, packs them into a tuple
# **kwargs (keyword arg): catches any named arguments (key=value),
# and packs them into a dict

def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    def combined_spell(*args, **kwargs) -> tuple[Any, Any]:
        return (spell1(*args, **kwargs), spell2(*args, **kwargs))
    return combined_spell


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    def amplified_spell(*args, **kwargs) -> int:
        return base_spell(*args, **kwargs) * multiplier
    return amplified_spell


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    def cast_if_true(*args, **kwargs) -> Any:
        if condition(*args, **kwargs):
            return spell(*args, **kwargs)
        return "Spell fizzled"
    return cast_if_true


def spell_sequence(spells: list[Callable]) -> Callable:
    def cast_sequence(*args, **kwargs) -> list[Any]:
        return [spell(*args, **kwargs) for spell in spells]
    return cast_sequence


def main():
    def fireball(target: str) -> str:
        return f"Fireball hits {target}"

    def heal(target: str) -> str:
        return f"Heals {target}"

    def basic_damage() -> int:
        return 10

    def is_enemy(target: str) -> bool:
        if target == "Knight":
            return False
        return True

    print("Testing spell combiner...")
    combined = spell_combiner(
        spell1=fireball,
        spell2=heal
    )
    result1, result2 = combined(target="Dragon")
    print(f"Combined spell result: {result1}, {result2}")
    print()

    print("Testing power amplifier...")
    mega_spell = power_amplifier(
        base_spell=basic_damage,
        multiplier=3
    )
    print(f"Original: {basic_damage()}, Amplified: {mega_spell()}")
    print()

    print("Testing conditional caster...")
    enemy_spell = conditional_caster(
        condition=is_enemy,
        spell=fireball
    )
    print(f"When target is Goblin (enemy): {enemy_spell(target='Goblin')}")
    print(f"When target is Knight (ally): {enemy_spell(target='Knight')}")
    print()

    print("Testing spell sequence...")
    sequence = spell_sequence(
        spells=[fireball, heal, heal, fireball]
    )
    results = sequence(target="Goblin")
    print(f"Spell sequence results: {', '.join(results)}")


if __name__ == "__main__":
    main()

# 1. How do higher-order functions enable code reuse and composition?

# "Instead of writing ten different combinations of spells (like a
# fire_and_heal function, an ice_and_heal function, etc.), I can write
#  a single spell_combiner higher-order function. It acts as a modular
#   'glue' that lets me combine any two existing functions in the game
#    dynamically, saving hundreds of lines of code."

# 2. What makes functions "first-class citizens" in Python?

# "It means Python treats functions exactly like it treats integers,
#  strings, or lists. Because they are just objects in memory, I can assign
#   a function to a variable, pass it into a function's arguments, and
#   return it as a result."
