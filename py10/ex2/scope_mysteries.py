from typing import Callable


def mage_counter() -> Callable:
    count = 0

    def count_up():
        nonlocal count
        count += 1
        return count

    return count_up


def spell_accumulator(initial_power: int) -> Callable:
    total_power = initial_power

    def accumulate(amount: int):
        nonlocal total_power
        total_power += amount
        return total_power

    return accumulate


def enchantment_factory(enchantment_type: str) -> Callable:
    def enchant(item_name: str):
        return f"{enchantment_type} {item_name}"

    return enchant


def memory_vault() -> dict[str, Callable]:
    vault_storage = {}

    def store(key: str, value: str):
        vault_storage[key] = value

    def recall(key: str):
        return vault_storage.get(key, "Memory not found")

    return {'store': store, 'recall': recall}


def main():
    try:
        my_counter = mage_counter()
        print(
            "Testing mage counter...\n"
            f"Call 1: {my_counter()}\n"
            f"Call 2: {my_counter()}\n"
            f"Call 3: {my_counter()}"
        )
        print()

        my_accumulator = spell_accumulator(100)
        print(
            "Testing spell accumulator...\n"
            f"Initial power: 100\n"
            f"After adding 20: {my_accumulator(20)}\n"
            f"After adding 30: {my_accumulator(30)}\n"
            f"After adding 50: {my_accumulator(50)}"
        )
        print()

        fire_enchanter = enchantment_factory("Flaming")
        ice_enchanter = enchantment_factory("Frozen")

        print(
            "Testing enchantment factory...\n"
            f"{fire_enchanter('Sword')}\n"
            f"{ice_enchanter('Shield')}"
        )
        print()

        vault = memory_vault()
        vault['store']("secret_spell", "Invisibility")
        print(
            "Testing memory vault...\n"
            f"Recalling 'secret_spell': {vault['recall']('secret_spell')}\n"
            f"Recalling 'non_existent': {vault['recall']('non_existent')}"
        )

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

# lexical scoping: inner functions can look "outward" and see the
# outer function's variables, but not the other way around

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
