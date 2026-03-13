from ex0.CreatureCard import CreatureCard
from .SpellCard import SpellCard
from .ArtifactCard import ArtifactCard
from .Deck import Deck


def main() -> None:
    print("=== Data Deck Builder ===")
    print()
    print("Building deck with different card types...")
    deck = Deck()
    deck.add_card(SpellCard(
        name="Lightning Bolt",
        cost=3,
        rarity="Common",
        effect_type="damage"
    ))
    deck.add_card(ArtifactCard(
        name="Mana Crystal",
        cost=2,
        rarity="Rare",
        durability=5,
        effect="+1 mana per turn"
    ))
    deck.add_card(CreatureCard(
        name="Fire Dragon",
        cost=5,
        rarity="Legendary",
        attack=7,
        health=5
    ))

    print(f"Deck stats: {deck.get_deck_stats()}")
    print()

    print("Drawing and playing cards:")
    print()

    for _ in range(3):
        card = deck.draw_card()
        if card:
            print(f"Drew: {card.name} ({card.type})")
            print(f"Play result: {card.play({})}")
            print()

    print("Polymorphism in action: Same interface, different card behaviors!")


if __name__ == "__main__":
    main()
