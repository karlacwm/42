from .CreatureCard import CreatureCard
from typing import Any


def main() -> None:
    print("=== DataDeck Card Foundation ===")
    print()
    print("Testing Abstract Base Class Design:")
    print()

    try:
        fire_dragon = CreatureCard(
            name="Fire Dragon",
            cost=5,
            rarity="Legendary",
            attack=7,
            health=5
        )

        goblin_warrior = CreatureCard(
            name="Goblin Warrior",
            cost=2,
            rarity="Common",
            attack=3,
            health=2
        )
    except ValueError as e:
        print(f"Error creating card: {e}")
        return

    mana_available = 6

    card_info: dict[str, Any] = fire_dragon.get_card_info()
    print(f"CreatureCard Info:\n{card_info}")
    print()

    print(f"Playing {fire_dragon.name} with {mana_available} mana available:")
    game_state: dict[str, Any] = {}
    print(f"Playable: {fire_dragon.is_playable(mana_available)}")
    print(f"Play result: {fire_dragon.play(game_state)}")
    print()

    print(f"{fire_dragon.name} attacks {goblin_warrior.name}:")
    print(f"Attack result: {fire_dragon.attack_target(goblin_warrior.name)}")
    print()

    print("Testing insufficient mana (3 available):")
    mana_available = 3
    print(f"Playable: {fire_dragon.is_playable(mana_available)}")
    print()

    print("Abstract pattern successfully demonstrated!")


if __name__ == "__main__":
    main()
