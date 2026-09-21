from typing import Callable
import time
import functools
import inspect


def spell_timer(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Casting {func.__name__}...")
        start_time = time.time()

        result = func(*args, **kwargs)

        end_time = time.time()
        print(f"Spell completed in {end_time - start_time:.3f} seconds")
        return result
    return wrapper


def power_validator(min_power: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            bound_args = inspect.signature(func).bind(*args, **kwargs)
            bound_args.apply_defaults()
            power = bound_args.arguments.get('power', 0)

            if power >= min_power:
                return func(*args, **kwargs)
            return "Insufficient power for this spell"
        return wrapper
    return decorator


def retry_spell(max_attempts: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    print(
                        f"Spell failed, retrying... (attempt {attempt}/{max_attempts})")
            return f"Spell casting failed after {max_attempts} attempts"
        return wrapper
    return decorator


class MageGuild:

    @staticmethod
    def validate_mage_name(name: str) -> bool:
        if len(name) < 3:
            return False
        # Check if every character is either a letter or a space
        return all(char.isalpha() or char.isspace() for char in name)

    @power_validator(min_power=10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


def main():
    print("Testing spell timer...")

    @spell_timer
    def fireball():
        time.sleep(0.1)
        return "Fireball cast!"

    print(f"Result: {fireball()}")
    print()

    print("Testing MageGuild...")
    print(MageGuild.validate_mage_name("Gandalf the White"))
    print(MageGuild.validate_mage_name("A!"))

    guild = MageGuild()
    print(guild.cast_spell("Lightning", 15))
    print(guild.cast_spell("Frost Nova", 5))


if __name__ == "__main__":
    main()
# 1. How do decorators enable separation of concerns?

# "They allow me to extract generic logic (like logging, timing,
# validation, or retry loops) out of my core business logic.
# My cast_spell function only has to worry about casting a spell.
#  It doesn't have to clutter its code with if power < 10 checks.
#  The decorator acts as a bouncer at the door, ensuring the core
#   function stays perfectly clean."

# 2. What's the difference between @staticmethod and regular instance methods?

# "A regular instance method must take self as its first argument because
# it needs to read or modify the object's internal data. A @staticmethod
#  does not take self. It's just a regular utility function that happens
#   to live inside the class namespace because it is logically related
#   to the class (like validating a name before creating a Mage), but it
#    doesn't need to access any specific Mage's data."
