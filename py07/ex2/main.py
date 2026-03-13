from ex2.EliteCard import EliteCard

def main() -> None:
    print("=== DataDeck Ability System ===")
    print("EliteCard capabilities:")
    print("Card: ['play', 'get_card_info', 'is_playable']")
    print("Combatable: ['attack', 'defend', 'get_combat_stats']")
    print("Magical: ['cast_spell', 'channel_mana', 'get_magic_stats']")

    print("\nPlaying Arcane Warrior (Elite Card):")
    # Cost: 6, Attack: 5, Health: 10
    warrior = EliteCard("Arcane Warrior", 6, "Epic", 5, 10)

    print("Combat phase:")
    print(f"Attack result: {warrior.attack('Enemy')}")
    # Simulating taking 5 damage (3 blocked, 2 taken)
    print(f"Defense result: {warrior.defend(5)}")

    print("Magic phase:")
    print(f"Spell cast: {warrior.cast_spell('Fireball', ['Enemy1', 'Enemy2'])}")
    print(f"Mana channel: {warrior.channel_mana(3)}"


if __name__ == "__main__":
    main()

# 1. How do multiple interfaces enable flexible card design?

# "It treats abilities like LEGO blocks. Instead of creating
# a massive, deep inheritance tree (like class MagicFightingCard(MagicCard,
# FightingCard)), I can just snap on the Magical interface and the Combatable
# interface to any new card I invent. It makes the code infinitely scalable."

# 2. What are the advantages of separating combat and magic concerns?

# "It follows the Single Responsibility Principle and the Interface
# Segregation Principle (from SOLID). A basic sword card doesn't need
# to know how to cast spells. By keeping Combatable and Magical as separate
# files, cards only inherit the specific logic they actually need, keeping
# the system lightweight and bug-free."
