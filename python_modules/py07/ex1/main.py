from ex0.CreatureCard import CreatureCard
from .SpellCard import SpellCard
from .ArtifactCard import ArtifactCard
from .Deck import Deck
from typing import Any


def main() -> None:
    print("=== Data Deck Builder ===")
    print()
    print("Building deck with different card types...")
    try:
        lightnig_bolt = SpellCard(
            name="Lightning Bolt",
            cost=3,
            rarity="Common",
            effect_type="damage"
        )
        mana_crystal = ArtifactCard(
            name="Mana Crystal",
            cost=2,
            rarity="Rare",
            durability=5,
            effect="+1 mana per turn"
        )
        fire_dragon = CreatureCard(
            name="Fire Dragon",
            cost=5,
            rarity="Legendary",
            attack=7,
            health=5
        )
    except ValueError as e:
        print(f"Error creating card: {e}")
        return

    cards = [lightnig_bolt, mana_crystal, fire_dragon]
    deck = Deck()
    for card in cards:
        deck.add_card(card)

    print(f"Deck stats: {deck.get_deck_stats()}")
    print()

    print("Drawing and playing cards:")
    print()

    game_state: dict[str, Any] = {}
    for _ in range(3):
        try:
            card = deck.draw_card()
        except IndexError:
            print("Deck is empty, no more cards to draw.")
            break
        if card:
            print(f"Drew: {card.name} ({card.type})")
            print(f"Play result: {card.play(game_state)}")
            print()

    print("Polymorphism in action: Same interface, different card behaviors!")


if __name__ == "__main__":
    main()
