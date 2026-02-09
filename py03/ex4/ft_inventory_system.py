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
        percentage: float = sorted_inventory[i] / total_items * 100
        if sorted_inventory[i] > 1:
            print(f"{i}: {sorted_inventory[i]} units ({percentage:.1f}%)")
        else:
            print(f"{i}: {sorted_inventory[i]} unit ({percentage:.1f}%)")
    print()
    print("=== Inventory Statistics ===")
    inventory_list = list(sorted_inventory)
    most: int = max(sorted_inventory.values())
    least: int = min(sorted_inventory.values())
    if most > 1:
        print("Most abundant:", inventory_list[0], f"({most} units)")
    else:
        print("Most abundant:", inventory_list[0], f"({most} unit)")
    if least > 1:
        print("Least abundant:", inventory_list[(len(inventory_list) - 1)],
              f"({least} units)")
    else:
        print("Least abundant:", inventory_list[(len(inventory_list) - 1)],
              f"({least} unit)")
    print()
    print("=== Item Categories ===")
    moderate_int: dict[str, int] = {}
    scarce_int: dict[str, int] = {}
    organised_inventory: dict[str, dict[str, int]] = {
        "moderate": moderate_int,
        "scarce": scarce_int
    }
    for i in inventory:
        if inventory[i] < 5:
            scarce_int[i] = inventory[i]
        else:
            moderate_int[i] = inventory[i]
    print("Moderate:", organised_inventory["moderate"])
    print("Scarce:", organised_inventory["scarce"])
    print()
    print("=== Management Suggestions ===")
    restock = {}
    for i in scarce_int:
        if scarce_int[i] < 2:
            restock[i] = scarce_int[i]
    print("Restock needed:", list(restock.keys()))
    print()
    print("=== Dictionary Properties Demo ===")
    all_keys: list[str] = list(inventory.keys())
    all_values: list[int] = list(inventory.values())
    lookup_item = "sword"
    lookup = inventory.get(lookup_item)
    if lookup is not None:
        lookup = True
    else:
        lookup = False
    print(f"Dictionary keys: {all_keys}")
    print(f"Dictionary values: {all_values}")
    print(f"Sample lookup - '{lookup_item}' in inventory: {lookup}")


if __name__ == "__main__":
    inventory_system()
