from typing import Callable


def mage_counter() -> Callable[[], int]:
    count = 0

    def count_up() -> int:
        nonlocal count
        count += 1
        return count

    return count_up


def spell_accumulator(initial_power: int) -> Callable[[int], int]:
    total_power = initial_power

    def accumulate(amount: int) -> int:
        nonlocal total_power
        total_power += amount
        return total_power

    return accumulate


def enchantment_factory(enchantment_type: str) -> Callable[[str], str]:
    def enchant(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"

    return enchant


def memory_vault() -> dict[str, Callable]:
    vault_storage = {}

    def store(key: str, value: str) -> None:
        vault_storage[key] = value

    def recall(key: str) -> str:
        return vault_storage.get(key, "Memory not found")

    return {'store': store, 'recall': recall}


def main() -> None:
    try:
        my_counter = mage_counter()
        print("Testing mage counter...")
        print(f"Call 1: {my_counter()}")
        print(f"Call 2: {my_counter()}")
        print(f"Call 3: {my_counter()}")
        print()

        my_accumulator = spell_accumulator(100)
        print("Testing spell accumulator...")
        print(f"Initial power: 100")
        print(f"After adding 20: {my_accumulator(20)}")
        print(f"After adding 30: {my_accumulator(30)}")
        print(f"After adding 50: {my_accumulator(50)}")
        print()

        fire_enchanter = enchantment_factory("Flaming")
        ice_enchanter = enchantment_factory("Frozen")

        print(
            "Testing enchantment factory...")
        print(fire_enchanter('Sword'))
        print(ice_enchanter('Shield'))
        print()

        vault = memory_vault()
        vault['store']("secret_spell", "Invisibility")
        print("Testing memory vault...")
        print(f"Recalling 'secret_spell': {vault['recall']('secret_spell')}")
        print(f"Recalling 'non_existent': {vault['recall']('non_existent')}")
        print()

    except Exception as e:
        print(f"There is an error: {e}")


if __name__ == "__main__":
    main()

# lexical scoping: inner functions can look "outward" and see the
# outer function's variables, but not the other way around

# closure: created when an outer function returns the inner function
# instead of executing it

# nonlocal: allows inner function to modify variables in outer scope,
# without nonlocal, python assumes you are trying to create a new
# local variable with the same name, and it crashes


# 1. How do closures enable functions to "remember" their creation environment?

# "When an inner function references variables from its outer function,
# Python takes those variables and bundles them together with the inner
# function into a single object called a closure. Even after the outer
# function finishes executing and returns, that bundle of variables is
#  kept alive in memory as long as the inner function still exists."

# 2. What are the benefits of lexical scoping in functional programming?

# "It allows us to maintain state and privacy without resorting to global
# variables or writing full Object-Oriented classes. For example, in our
# memory_vault(), the vault_storage dictionary is completely hidden from
#  the outside world. The only way to interact with it is through the
#  specific store and recall functions we provided, which creates perfect
#   data encapsulation."
