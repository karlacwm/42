from ex3 import AggressiveStrategy, FantasyCardFactory, GameEngine


def format_hand(hand: list) -> list[str]:
    result = []
    for card in hand:
        result.append(f"{card.name} ({card.cost})")
    return result


def main() -> None:
    print("=== DataDeck Game Engine ===")
    print()

    cards = {
        "dragon": ("Fire Dragon", 5, "Legendary", 8, 8),
        "goblin": ("Goblin Warrior", 2, "Common", 3, 2),
    }
    spells = {
        "fireball": ("Fireball", 4, "Rare", "Burn"),
        "lightning": ("Lightning Bolt", 3, "Rare", "Shock"),
        "ice": ("Ice Lance", 2, "Common", "Freeze"),
    }
    artifacts = {
        "mana_ring": ("Mana Ring", 1, "Uncommon", 3, "+1 mana each turn"),
        "arcane_staff": ("Arcane Staff", 3, "Rare", 4, "Boost spell power"),
        "crystal": ("Aether Crystal", 2, "Common", 2, "Store magical charge"),
    }
    deck_order = [
        ("creature", "dragon"),
        ("creature", "goblin"),
        ("spell", "fireball"),
        ("spell", "lightning"),
        ("artifact", "mana_ring"),
    ]

    spell_damage = {
        "Lightning Bolt": 5,
        "Fireball": 4,
        "Ice Lance": 3,
    }
    mana_limit = 5
    enemy_tag = "Enemy"
    default_targets = ["Enemy Player"]

    factory = FantasyCardFactory(
        cards=cards,
        spells=spells,
        artifacts=artifacts,
        deck_order=deck_order,
    )
    strategy = AggressiveStrategy(
        mana_limit=mana_limit,
        spell_damage=spell_damage,
        enemy_tag=enemy_tag,
        default_targets=default_targets,
    )
    engine = GameEngine()
    engine.configure_engine(factory, strategy)

    hand = [
        factory.create_creature("dragon"),
        factory.create_creature("goblin"),
        factory.create_spell("lightning"),
    ]
    battlefield = ["Enemy Creature", "Enemy Player"]
    engine.current_hand = hand
    engine.current_battlefield = battlefield

    print("Configuring Fantasy Card Game...")
    print(f"Factory: {factory.__class__.__name__}")
    print(f"Strategy: {strategy.get_strategy_name()}")
    print(f"Available types: {factory.get_supported_types()}")
    print()

    print("Simulating aggressive turn...")
    actions = engine.simulate_turn()
    print(f"Hand: {format_hand(hand)}")
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



#How do Abstract Factory and Strategy patterns work together? 
# What makes this combination powerful for game engine systems?".

# The Answer: "They perfectly separate creation from behavior. 
# The Abstract Factory handles all the messy logic of spawning the right cards
#  (creation), while the Strategy handles the AI logic of playing them 
# (behavior). Because the GameEngine relies purely on abstract interfaces 
# instead of concrete classes, I could swap in a SciFiCardFactory and a
#  DefensiveStrategy without changing a single line of code in the Game Engine 
# itself. This makes the system incredibly modular, plug-and-play, 
# and easy to scale!"
