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

    try:
        arcane_warrior = EliteCard(
            name="Arcane Warrior",
            cost=6,
            rarity="Epic",
            attack=5,
            health=10
        )
    except ValueError as e:
        print(f"Error creating card: {e}")
        return

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
