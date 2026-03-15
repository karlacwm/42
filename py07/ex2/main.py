from ex0.Card import Card
from ex2.EliteCard import EliteCard
from ex2.Combatable import Combatable
from ex2.Magical import Magical


def elitecard_capabilities() -> None:
    print("EliteCard capabilities:")
    card_method = [method for method in dir(
        Card) if not method.startswith('_')]
    print(f"- Card: {card_method}")
    combatable_method = [method for method in dir(
        Combatable) if not method.startswith('_')]
    print(f"- Combatable: {combatable_method}")
    magical_method = [method for method in dir(
        Magical) if not method.startswith('_')]
    print(f"- Magical: {magical_method}")


def main() -> None:
    print("=== DataDeck Ability System ===")
    print()
    elitecard_capabilities()
    print()

    print("Playing Arcane Warrior (Elite Card):")
    print()

    arcane_warrior = EliteCard(
        name="Arcane Warrior",
        cost=6,
        rarity="Epic",
        attack=5,
        health=10
    )

    print("Combat phase:")
    print(f"Attack result: {arcane_warrior.attack(target='Enemy')}")
    print(f"Defense result: {arcane_warrior.defend(incoming_damage=5)}")
    print()

    print("Magic phase:")
    spell_cast = arcane_warrior.cast_spell(
        spell_name='Fireball',
        targets=['Enemy1', 'Enemy2'],
    )
    print(
        f"Spell cast: {spell_cast}")
    print(f"Mana channel: {arcane_warrior.channel_mana(amount=3)}")
    print()

    print("Multiple interface implementation successful!")


if __name__ == "__main__":
    main()


# https://www.askpython.com/python/examples/find-all-methods-of-class


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
