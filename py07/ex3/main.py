from typing import Any
from ex0.Card import Card
from ex3.AggressiveStrategy import AggressiveStrategy
from ex3.GameEngine import GameEngine
from ex3.FantasyCardFactory import FantasyCardFactory


def format_hand(hand: list[Card]) -> list[str]:
    result = []
    for card in hand:
        result.append(f"{card.name} ({card.cost})")
    return result


def main() -> None:
    print("=== DataDeck Game Engine ===")
    print()

    spell_damage = {
        "Lightning Bolt": 5,
        "Fireball": 4,
        "Ice Shard": 3,
    }
    mana_limit = 5
    enemy_tag = "Enemy"
    default_targets = ["Enemy Creature", "Enemy Player"]

    deck_order = [
        ("creature", "dragon"),
        ("spell", "fireball"),
        ("artifact", "mana_ring"),
        ("creature", "goblin"),
        ("spell", "lightning"),
        ("artifact", "crystals"),
        ("creature", "troll"),
        ("spell", "ice"),
        ("artifact", "staffs"),
    ]

    factory = FantasyCardFactory(deck_order=deck_order)
    strategy = AggressiveStrategy(
        mana_limit=mana_limit,
        spell_damage=spell_damage,
        enemy_tag=enemy_tag,
        default_targets=default_targets,
    )
    engine = GameEngine()
    engine.configure_engine(factory=factory, strategy=strategy)

    themed_deck_result = factory.create_themed_deck(size=50)
    themed_deck = themed_deck_result["deck"]
    hand: list[Card] = []
    for _ in range(3):
        hand.append(themed_deck.draw_card())

    battlefield = default_targets
    engine.current_hand = hand
    engine.current_battlefield = battlefield

    print("Configuring Fantasy Card Game...")
    print(f"Factory: {factory.__class__.__name__}")
    print(f"Strategy: {strategy.get_strategy_name()}")
    print(f"Available types: {factory.get_supported_types()}")
    print()

    print("Simulating aggressive turn...")
    actions: dict[str, Any] = {}
    try:
        actions = engine.simulate_turn()
    except RuntimeError as exc:
        print(f"Setup error: {exc}")
    print(f"Hand: {format_hand(hand=hand)}")
    print()

    print("Turn execution:")
    print(f"Strategy: {strategy.get_strategy_name()}")
    print(f"Actions: {actions}")
    print()

    print(f"Game Report:\n{engine.get_engine_status()}")
    print()
    print("Abstract Factory + Strategy Pattern: Maximum flexibility achieved!")


if __name__ == "__main__":
    main()


# How do Abstract Factory and Strategy patterns work together?
# What makes this combination powerful for game engine systems?".

# The Answer: "They perfectly separate creation from behavior.
# The Abstract Factory handles all the messy logic of spawning the right cards
#  (creation), while the Strategy handles the AI logic of playing them
# (behavior). Because the GameEngine relies purely on abstract interfaces
# instead of concrete classes, I could swap in a SciFiCardFactory and a
#  DefensiveStrategy without changing a single line of code in the Game Engine
# itself. This makes the system incredibly modular, plug-and-play,
# and easy to scale!"
