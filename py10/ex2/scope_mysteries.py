# ex2/scope_mysteries.py

def mage_counter() -> callable:
    """Returns a closure that counts how many times it's been called."""
    count = 0  # This variable will be "trapped" in the closure
    
    def counter():
        nonlocal count  # Tells Python we want to modify the outer 'count'
        count += 1
        return count
        
    return counter


def spell_accumulator(initial_power: int) -> callable:
    """Returns a closure that accumulates power over time."""
    total_power = initial_power
    
    def accumulate(amount: int):
        nonlocal total_power
        total_power += amount
        return total_power
        
    return accumulate


def enchantment_factory(enchantment_type: str) -> callable:
    """Returns a closure that applies a specific enchantment type."""
    # We don't need 'nonlocal' here because we are only reading the variable, not modifying it.
    def enchant(item_name: str):
        return f"{enchantment_type} {item_name}"
        
    return enchant


def memory_vault() -> dict[str, callable]:
    """Returns a dict of functions sharing the same private memory storage."""
    vault_storage = {}  # Private dictionary trapped in the closure
    
    def store(key: str, value):
        # Dictionaries are mutable, so we don't need 'nonlocal' to add keys to it!
        vault_storage[key] = value
        
    def recall(key: str):
        return vault_storage.get(key, "Memory not found")
        
    return {'store': store, 'recall': recall}


if __name__ == "__main__":
    # --- Testing Logic to Match Expected Output ---
    
    print("Testing mage counter...")
    # We create the counter. 'count' is set to 0 and trapped inside my_counter.
    my_counter = mage_counter()
    print(f"Call 1: {my_counter()}")
    print(f"Call 2: {my_counter()}")
    print(f"Call 3: {my_counter()}")
    
    print("Testing enchantment factory...")
    # We create two completely separate closures, each remembering a different string!
    fire_enchanter = enchantment_factory("Flaming")
    ice_enchanter = enchantment_factory("Frozen")
    
    print(fire_enchanter("Sword"))
    print(ice_enchanter("Shield"))



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