from typing import Callable, Any


# * and ** are unpacking operators when not used in math
# * for lists and tuples, ** for dicts
# *args and **kwargs: dont know how many arguments, but just catch them all
# *args (arguments): catches any arguments, packs them into a tuple
# **kwargs (keyword arg): catches any named arguments (key=value),
# and packs them into a dict

def spell_combiner(
        spell1: Callable[[str], str],
        spell2: Callable[[str], str]) -> Callable[[str], tuple[str, str]]:
    def combined_spell(target: str) -> tuple[str, str]:
        return (spell1(target), spell2(target))
    return combined_spell


def power_amplifier(
        base_spell: Callable[[], int],
        multiplier: int) -> Callable[[], int]:
    def amplified_spell(*args: Any, **kwargs: Any) -> int:
        return base_spell(*args, **kwargs) * multiplier
    return amplified_spell


def conditional_caster(
        condition: Callable[[Any], bool],
        spell: Callable[[Any], Any]) -> Callable[[Any], Any]:
    def cast_if_true(*args: Any, **kwargs: Any) -> Any:
        if condition(*args, **kwargs):
            return spell(*args, **kwargs)
        return "Spell fizzled"
    return cast_if_true


def spell_sequence(
        spells: list[Callable[[Any], Any]]) -> Callable[[Any], list[Any]]:
    def cast_sequence(*args: Any, **kwargs: Any) -> list[Any]:
        return [spell(*args, **kwargs) for spell in spells]
    return cast_sequence


def main() -> None:
    def fireball(target: str) -> str:
        return f"Fireball hits {target}"

    def heal(target: str) -> str:
        return f"Heals {target}"

    def stun(target: str) -> str:
        return f"Stuns {target}"

    def trap(target: str) -> str:
        return f"Traps {target}"

    def basic_damage() -> int:
        return 10

    def is_enemy(target: str) -> bool:
        if target == "Knight":
            return False
        return True

    try:
        combined = spell_combiner(
            spell1=fireball,
            spell2=heal
        )
        result1, result2 = combined("Dragon")
        print("Testing spell combiner...")
        print(f"Combined spell result: {result1}, {result2}")
        print()

        mega_spell = power_amplifier(
            base_spell=basic_damage,
            multiplier=3
        )
        print("Testing power amplifier...")
        print(f"Original: {basic_damage()}, Amplified: {mega_spell()}")
        print()

        enemy_spell = conditional_caster(
            condition=is_enemy,
            spell=fireball
        )
        print("Testing conditional caster...")
        print(f"When target is Goblin (enemy): {enemy_spell('Goblin')}")
        print(f"When target is Knight (ally): {enemy_spell('Knight')}")
        print()

        sequence = spell_sequence(
            spells=[stun, trap, fireball, stun]
        )
        results = sequence("Goblin")
        print("Testing spell sequence...")
        print(f"Spell sequence results: {', '.join(results)}")

    except Exception as e:
        print(f"Error caught: {e}")


if __name__ == "__main__":
    main()


# higher order functions: functions that can take other functions as
# arguments, or return them as results


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
