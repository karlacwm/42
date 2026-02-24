def absolute_imports() -> None:
    from alchemy.transmutation.basic import lead_to_gold, stone_to_gem
    print("Testing Absolute Imports (from basic.py):")
    print(f"lead_to_gold(): {lead_to_gold()}")
    print(f"stone_to_gem(): {stone_to_gem()}")
    print()


def relative_imports() -> None:
    print("Testing Relative Imports (from advanced.py):")
    from alchemy.transmutation.advanced import philosophers_stone, elixir_of_life
    print(f"philosophers_stone(): {philosophers_stone()}")
    print(f"elixir_of_life(): {elixir_of_life()}")
    print()


def package_access() -> None:
    import alchemy
    print("Testing Package Access:")
    print(f"alchemy.transmutation.lead_to_gold(): {alchemy.transmutation.lead_to_gold()}")
    print(f"alchemy.transmutation.philosophers_stone(): {alchemy.transmutation.philosophers_stone()}")
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