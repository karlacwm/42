# ex1/higher_magic.py

def spell_combiner(spell1: callable, spell2: callable) -> callable:
    """Returns a new function that casts both spells and returns a tuple of results."""
    def combined_spell(*args, **kwargs):
        # Calls both spells with whatever arguments are passed in
        return (spell1(*args, **kwargs), spell2(*args, **kwargs))
    return combined_spell


def power_amplifier(base_spell: callable, multiplier: int) -> callable:
    """Returns a new function that multiplies the base spell's result."""
    def amplified_spell(*args, **kwargs):
        # Gets the original result (a number) and multiplies it
        return base_spell(*args, **kwargs) * multiplier
    return amplified_spell


def conditional_caster(condition: callable, spell: callable) -> callable:
    """Returns a new function that casts the spell only if the condition is True."""
    def cast_if_true(*args, **kwargs):
        # Both condition and spell receive the exact same arguments
        if condition(*args, **kwargs):
            return spell(*args, **kwargs)
        return "Spell fizzled"
    return cast_if_true


def spell_sequence(spells: list[callable]) -> callable:
    """Returns a new function that casts all spells in order."""
    def cast_sequence(*args, **kwargs):
        # Uses a list comprehension to run every spell in the list
        return [spell(*args, **kwargs) for spell in spells]
    return cast_sequence


if __name__ == "__main__":
    # --- Testing Logic to Match Expected Output ---
    
    # Dummy spell functions for testing
    def cast_fireball(target):
        return f"Fireball hits {target}"
        
    def cast_heal(target):
        return f"Heals {target}"
        
    def basic_damage():
        return 10
        
    print("Testing spell combiner...")
    # spell_combiner returns a BRAND NEW function, which we save to a variable
    combined = spell_combiner(cast_fireball, cast_heal)
    # Now we call our new function
    result1, result2 = combined("Dragon")
    print(f"Combined spell result: {result1}, {result2}")
    
    print("Testing power amplifier...")
    # power_amplifier returns a new function that multiplies the output by 3
    mega_spell = power_amplifier(basic_damage, 3)
    print(f"Original: {basic_damage()}, Amplified: {mega_spell()}")


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