from .CreatureCard import CreatureCard
from typing import Any


def main() -> None:
    print("=== DataDeck Card Foundation ===")
    print()
    print("Testing Abstract Base Class Design:")
    print()

    fire_dragon = CreatureCard(
        name="Fire Dragon",
        cost=5,
        rarity="Legendary",
        attack=7,
        health=5
    )
    card_info: dict[str, Any] = fire_dragon.get_card_info()
    print(f"CreatureCard Info: {card_info}")
    print()

    print("Playing Fire Dragon with 6 mana available:")
    game_state: dict[str, Any] = {}
    print(f"Playable: {fire_dragon.is_playable(6)}")
    print(f"Play result: {fire_dragon.play(game_state)}")
    print()

    print("Fire Dragon attacks Goblin Warrior:")
    print(f"Attack result: {fire_dragon.attack_target('Goblin Warrior')}")
    print()

    print("Testing insufficient man (3 available):")
    print(f"Playable: {fire_dragon.is_playable(3)}")
    print()

    print("Abstract pattern successfully demonnstrated!")


if __name__ == "__main__":
    main()


# How do abstract base classes ensure consistency across different
# card types? What happens if you try to create a Card directly
# without implementing required methods?

# Abstract Base Classes (ABCs) act as a strict legal contract. By
# defining methods with @abstractmethod, we force any future developer
# who creates a new card type (like a SpellCard or ArtifactCard) to write
# their own version of the play() function. This guarantees that the Game
# Engine can confidently loop through a list of 1,000 completely different
# cards and call card.play() on every single one of them without the program
# ever crashing.
# Python actively protects you! If you attempt to write my_card = Card("Test",
#  1, "Common") directly in your main.py file, Python will immediately crash
# and throw a TypeError: Can't instantiate abstract class Card with abstract
# methods play.
