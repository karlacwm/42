from typing import Any


# lambda x: 42 * x
# (no function name, just lambda)(parameter): (return value)
def artifact_sorter(artifacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    # sorted() can use a lambda as a key for custom sorting
    # reverse=True makes it descending
    return sorted(artifacts, key=lambda artifact: artifact["power"],
                  reverse=True)


def power_filter(
        mages: list[dict[str, Any]], min_power: int) -> list[dict[str, Any]]:
    # filter() creates a list of items for which a function returns True
    # wrap it in list() to convert the result from an iterator back to a list
    return list(filter(lambda mage: mage["power"] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    # map() applies a function to every item in an iterable
    return list(map(lambda spell: f"* {spell} *", spells))


def mage_stats(mages: list[dict[str, Any]]) -> dict[str, int | float]:
    if not mages:
        return {"max_power": 0, "min_power": 0, "avg_power": 0.0}

    power_list = list(map(lambda x: x['power'], mages))
    return {
        'max_power': max(power_list),
        'min_power': min(power_list),
        'avg_power': round(sum(power_list) / len(power_list), 2) if (
            power_list) else 0.0
    }


class SpellCaster:
    def __init__(self) -> None:
        self.artifacts = [
            {'name': 'Light Prism', 'power': 75, 'type': 'weapon'},
            {'name': 'Fire Staff', 'power': 95, 'type': 'focus'},
            {'name': 'Crystal Orb', 'power': 85, 'type': 'relic'},
            {'name': 'Earth Shield', 'power': 65, 'type': 'armor'}
        ]

        self.spells = ["fireball", "heal", "shield"]

        self.mages = [
            {'name': 'Rowan', 'power': 92, 'element': 'fire'},
            {'name': 'Zara', 'power': 82, 'element': 'wind'},
            {'name': 'Luna', 'power': 97, 'element': 'fire'},
            {'name': 'Ash', 'power': 87, 'element': 'ice'},
            {'name': 'Sage', 'power': 107, 'element': 'fire'}
        ]

    def sorter(self) -> None:
        print("Testing artifact_sorter...")
        sorted_artifacts = artifact_sorter(self.artifacts)
        first = sorted_artifacts[0]
        second = sorted_artifacts[1]
        print(f"{first['name']} ({first['power']} power) comes before "
              f"{second['name']} ({second['power']} power)")
        print()

    def spell_transformer(self) -> None:
        print("Testing spell_transformer...")
        transformed_spells = spell_transformer(self.spells)
        print(*transformed_spells)

    def filter(self) -> None:
        print()
        min_power = 90
        print("Testing power filter...")
        filtered_mages = power_filter(self.mages, min_power)
        for mage in filtered_mages:
            print(f"{mage['name']} has at least "
                  f"{min_power} power ({mage['power']})")

    def stats(self) -> None:
        print()
        stats = mage_stats(self.mages)
        print(
            "Testing mage_stats...\n"
            f"Max Power: {stats['max_power']}\n"
            f"Min Power: {stats['min_power']}\n"
            f"Avg Power: {stats['avg_power']}"
        )

    def demo(self) -> None:
        self.sorter()
        self.spell_transformer()
        self.filter()
        self.stats()


def main() -> None:
    try:
        spell_caster = SpellCaster()
        spell_caster.demo()
    except Exception as e:
        print(f"Error caught during spell casting: {e}")
        return


if __name__ == "__main__":
    main()


# 1. How do lambda expressions make code more concise?

# "They allow you to define simple, single-use transformation
# logic inline. Instead of writing a whole 3-line def block somewhere
# else in the file just to extract a dictionary key, you can do it
# right inside the sorted() or map() function call, saving space and
# keeping the logic exactly where it's used."

# 2. When should you use lambda vs. regular function definitions?

# "You should use a lambda for simple, one-line expressions that
# you only need to use once (like a sorting key or a basic map
# transformation). If the logic is complex, requires multiple lines,
# needs if/else error handling, or needs to be reused in multiple places,
#  you should always use a standard def function for readability."
