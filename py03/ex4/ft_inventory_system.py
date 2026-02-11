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
    total_items: int = 0
    for i in inventory:
        total_items += inventory[i]
    unique_items: int = len(inventory)
    print("=== Inventory System Analysis ===")
    print("Total items in inventory:", total_items)
    print("Unique item types:", unique_items)
    print()
    if len(inventory) < 1:
        print("Empty inventory! No further inventory data is available.")
        return
    sorted_inventory = []
    for item, quantity in inventory.items():
        sorted_inventory.append([item, quantity])
    n: int = len(sorted_inventory)
    for i in range(n):
        for j in range(0, n - i - 1):
            if sorted_inventory[j][1] < sorted_inventory[j + 1][1]:
                temp = sorted_inventory[j]
                sorted_inventory[j] = sorted_inventory[j + 1]
                sorted_inventory[j + 1] = temp
    print("=== Current Inventory ===")
    for item in sorted_inventory:
        name = item[0]
        unit = item[1]
        percentage: float = unit / total_items * 100
        if unit > 1:
            print(f"{name}: {unit} units ({percentage:.1f}%)")
        else:
            print(f"{name}: {unit} unit ({percentage:.1f}%)")
    print()
    print("=== Inventory Statistics ===")
    if len(sorted_inventory) > 0:
        most_item = sorted_inventory[0][0]
        most_count = sorted_inventory[0][1]
        least_item = sorted_inventory[-1][0]
        least_count = sorted_inventory[-1][1]
        if most_count > 1:
            print("Most abundant:", most_item, f"({most_count} units)")
        else:
            print("Most abundant:", most_item, f"({most_count} unit)")
        if least_count > 1:
            print("Least abundant:", least_item, f"({least_count} units)")
        else:
            print("Least abundant:", least_item, f"({least_count} unit)")
    else:
        print("Empty inventory! No most or least abundant items.")
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
