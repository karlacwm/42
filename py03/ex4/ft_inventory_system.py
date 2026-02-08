import sys


def parse_items(item: str) -> dict[str, int] | None:
    if ":" not in item:
        reject_item(item, 'Item is not formatted as "item:quantity".')
        return None
    name, quantity = item.split(":", 1)
    if not name:
        reject_item(item, "Item name cannot be empty.")
        return None
    if name.isdigit():
        reject_item(item, "Item name cannot be a number.")
        return None
    try:
        unit = int(quantity)
    except ValueError:
        reject_item(item, f"Item quantity '{quantity}' must be numbers.")
        return None
    if unit < 0:
        reject_item(item, f"Item quantity '{unit}' cannot be negative.")
        return None
    new_item: dict[str, int] = {}
    new_item[name] = unit
    return new_item


def reject_item(item: str, message: str) -> None:
    print(f"Error: {message}")
    print(f"Item '{item}' is not added to the inventory.", end="\n\n")


def get_quantity(item: tuple[str, int]) -> int:
    return item[1]


def inventory_system() -> None:
    if len(sys.argv) < 2:
        print("Empty input! No items added to the inventory.")
        return
    inventory: dict[str, int] = {}
    for arg in sys.argv[1:]:
        item_to_add: dict[str, int] | None = parse_items(arg)
        if item_to_add is not None:
            inventory.update(item_to_add)
    sorted_inventory: dict[str, int] = dict(
        sorted(inventory.items(), key=get_quantity, reverse=True))
    total_items: int = 0
    for i in sorted_inventory:
        total_items += sorted_inventory[i]
    unique_items: int = len(sorted_inventory)
    print("=== Inventory System Analysis ===")
    print("Total items in inventory:", total_items)
    print("Unique item types:", unique_items)
    print()
    print("=== Current Inventory ===")
    for i in sorted_inventory:
        if sorted_inventory[i] > 1:
            percentage: float = sorted_inventory[i] / total_items * 100
            print(f"{i}: {sorted_inventory[i]} units ({percentage:.1f}%)")
        else:
            print(f"{i}: {sorted_inventory[i]} unit ({percentage:.1f}%)")
    print()
    print("=== Inventory Statistics ===")
    print("Most abundant:", max(sorted_inventory.values()))
    print("Least abundant:")
    print()
    print("=== Item Categories ===")
    print("Moderate:")
    print("Scare:")
    print()
    print("=== Management Suggestions ===")
    print("Restock needed:")
    print()
    print("=== Dictionary Properties Demo ===")
    all_keys = sorted_inventory.keys()
    all_values = sorted_inventory.values()
    print(f"Dictionary keys: {all_keys}")
    print(f"Dictionary values: {all_values}")
    print("Sample lookup - ")


if __name__ == "__main__":
    inventory_system()
