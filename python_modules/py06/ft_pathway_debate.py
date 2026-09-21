# abosolute import
from alchemy.transmutation.basic import lead_to_gold, stone_to_gem
# relative improt defined in advanced.py
from alchemy.transmutation.advanced import (philosophers_stone,
                                            elixir_of_life)
# package accesss
import alchemy.transmutation


def absolute_imports() -> None:
    print("Testing Absolute Imports (from basic.py):")
    print(f"lead_to_gold(): {lead_to_gold()}")
    print(f"stone_to_gem(): {stone_to_gem()}")
    print()


def relative_imports() -> None:
    print("Testing Relative Imports (from advanced.py):")
    print(f"philosophers_stone(): {philosophers_stone()}")
    print(f"elixir_of_life(): {elixir_of_life()}")
    print()


def package_access() -> None:
    print("Testing Package Access:")
    print("alchemy.transmutation.lead_to_gold(): "
          f"{alchemy.transmutation.lead_to_gold()}")
    print("alchemy.transmutation.philosophers_stone(): "
          f"{alchemy.transmutation.philosophers_stone()}")
    print()


def ft_pathway_debate() -> None:
    print("=== Pathway Debate Mastery ===")
    print()
    absolute_imports()
    relative_imports()
    package_access()
    print("Both pathways work! Absolute: clear, Relative: concise")


if __name__ == "__main__":
    ft_pathway_debate()
