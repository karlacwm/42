# ex3/functools_artifacts.py
import functools
import operator

def spell_reducer(spells: list[int], operation: str) -> int:
    """Combines all spell powers into a single value using reduce."""
    # Map the string to the actual operator functions
    ops = {
        "add": operator.add,
        "multiply": operator.mul,
        "max": max,
        "min": min
    }
    # Apply functools.reduce to fold the list
    return functools.reduce(ops[operation], spells)


def partial_enchanter(base_enchantment: callable) -> dict[str, callable]:
    """Uses partial to freeze the power and element arguments."""
    # The base_enchantment expects (power, element, target)
    # We lock in the first two arguments (50, and the element string)
    return {
        'fire_enchant': functools.partial(base_enchantment, 50, 'Fire'),
        'ice_enchant': functools.partial(base_enchantment, 50, 'Ice'),
        'lightning_enchant': functools.partial(base_enchantment, 50, 'Lightning')
    }


@functools.lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    """Calculates Fibonacci with automatic caching (memoization)."""
    if n < 2:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> callable:
    """Creates a single dispatch system that changes behavior based on type."""
    
    @functools.singledispatch
    def base_spell(arg):
        return "Unknown spell type"
        
    @base_spell.register(int)
    def _(arg: int):
        return f"Deals {arg} damage"
        
    @base_spell.register(str)
    def _(arg: str):
        return f"Casts {arg} enchantment"
        
    @base_spell.register(list)
    def _(arg: list):
        return f"Multi-cast: {', '.join(str(x) for x in arg)}"
        
    # Return the fully configured dispatcher function
    return base_spell


if __name__ == "__main__":
    # --- Testing Logic to Match Expected Output ---
    
    print("Testing spell reducer...")
    test_spells = [10, 20, 30, 40]
    print(f"Sum: {spell_reducer(test_spells, 'add')}")
    print(f"Product: {spell_reducer(test_spells, 'multiply')}")
    print(f"Max: {spell_reducer(test_spells, 'max')}")
    
    print("\nTesting memoized fibonacci...")
    # Because of lru_cache, Fib(15) is instant instead of calculating 987 separate branches!
    print(f"Fib(10): {memoized_fibonacci(10)}")
    print(f"Fib(15): {memoized_fibonacci(15)}")



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