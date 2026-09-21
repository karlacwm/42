from typing import Callable, Any
import functools
import operator


def spell_reducer(spells: list[int], operation: str) -> int:
    ops = {
        "add": operator.add,
        "multiply": operator.mul,
        "max": max,
        "min": min
    }
    return functools.reduce(ops[operation], spells)


def partial_enchanter(base_enchantment: Callable[[int, str, str], str]) -> dict[str, Callable]:
    return {
        'fire_enchant': functools.partial(base_enchantment, 50, 'Fire'),
        'ice_enchant': functools.partial(base_enchantment, 50, 'Ice'),
        'lightning_enchant': functools.partial(base_enchantment, 50, 'Lightning')
    }


@functools.lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n < 2:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:

    @functools.singledispatch
    def base_spell(arg: Any) -> str:
        return "Unknown spell type"

    @base_spell.register(int)
    def _(arg: int) -> str:
        return f"Deals {arg} damage"

    @base_spell.register(str)
    def _(arg: str) -> str:
        return f"Casts {arg} enchantment"

    @base_spell.register(list)
    def _(arg: list) -> str:
        return f"Multi-cast: {', '.join(str(x) for x in arg)}"

    return base_spell


def main() -> None:
    try:
        test_spells = [10, 15, 50, 2]
        print("Testing spell reducer...")
        print(f"Spells: {test_spells}")
        print(f"Sum: {spell_reducer(test_spells, 'add')}")
        print(f"Product: {spell_reducer(test_spells, 'multiply')}")
        print(f"Max: {spell_reducer(test_spells, 'max')}")
        print(f"Min: {spell_reducer(test_spells, 'min')}")
        print()

        def base_enchantment(power: int, element: str, item: str) -> str:
            return f"{element} enchantment of {power} power on {item}"

        partial_enchanters = partial_enchanter(base_enchantment)
        print("Testing partial enchanter...")
        print(f"Fire enchant: {partial_enchanters['fire_enchant']('Sword')}")
        print(f"Ice enchant: {partial_enchanters['ice_enchant']('Shield')}")
        print(
            f"Lightning enchant: {partial_enchanters['lightning_enchant']('Staff')}")
        print()

        print("Testing memoized fibonacci...")
        print(f"Fib(10): {memoized_fibonacci(10)}")
        print(f"Fib(15): {memoized_fibonacci(15)}")
        print()

        dispatcher = spell_dispatcher()
        print("Testing spell dispatcher...")
        print(f"Int spell: {dispatcher(100)}")
        print(f"Str spell: {dispatcher('Invisibility')}")
        print(f"List spell: {dispatcher([10, 20, 30])}")
        print(f"Float spell: {dispatcher(3.14)}")
        print()

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

# 1. How does functools.reduce enable powerful data aggregation?

# "It abstracts away the loop mechanism. Instead of manually
# creating a temporary variable, iterating over a list, and
# updating the variable step-by-step, reduce recursively folds

#  the data together using whatever specific operation I provide
#   (like addition or multiplication), resulting in much cleaner,
#   mathematically pure code."

# 2. What are the performance benefits of memoization with lru_cache?

# "In a recursive function like Fibonacci, the same numbers are
# recalculated thousands of times. For example, calculating Fib(15)
# requires calculating Fib(2) hundreds of times. lru_cache intercepts
#  the function call, checks if Fib(2) was already calculated, and
#  instantly returns the saved memory result instead of running the
#   code again. It turns a slow exponential time algorithm into a
#   blazing fast linear time algorithm."
