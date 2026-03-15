import random
from typing import Any
from ex0.Card import Card
from ex0.CreatureCard import CreatureCard
from ex1.Deck import Deck
from ex1.ArtifactCard import ArtifactCard
from ex1.SpellCard import SpellCard
from ex3.CardFactory import CardFactory


class FantasyCardFactory(CardFactory):
    # creatures: name, cost, rarity, attack, health
    creatures: dict[str, tuple[str, int, str, int, int]] = {
        "dragon": ("Fire Dragon", 5, "Legendary", 8, 8),
        "goblin": ("Goblin Warrior", 2, "Common", 3, 2),
        "troll": ("Troll Brute", 4, "Common", 5, 6),
    }
    # spells: name, cost, rarity, effect_type
    spells: dict[str, tuple[str, int, str, str]] = {
        "fireball": ("Fireball", 4, "Common", "Burn"),
        "lightning": ("Lightning Bolt", 3, "Rare", "Shock"),
        "ice": ("Ice Shard", 2, "Common", "Freeze"),
    }
    # artifacts: name, cost, rarity, durability, effect
    artifacts: dict[str, tuple[str, int, str, int, str]] = {
        "mana_ring": ("Mana Ring", 1, "Uncommon", 3, "+1 mana each turn"),
        "staffs": ("Staff of Element", 3, "Legendary", 4, "Boost spell power"),
        "crystals": (
            "Mana Crystal", 2, "Common", 2, "Store magical charge"),
    }

    def __init__(
        self,
        deck_order: list[tuple[str, str]] | None = None,
    ) -> None:
        self.creatures: dict[str, tuple[str, int, str, int, int]] = dict(
            self.creatures)
        self.spells: dict[str, tuple[str, int, str, str]] = dict(
            self.spells)
        self.artifacts: dict[str, tuple[str, int, str, int, str]] = dict(
            self.artifacts)
        if deck_order is None:
            deck_order = []
        self.deck_order: list[tuple[str, str]] = deck_order

    def create_creature(self, name_or_power: str | int | None = None) -> Card:
        keys = list(self.creatures.keys())
        if isinstance(name_or_power, str):
            key = name_or_power.lower()
        elif isinstance(name_or_power, int):
            key = keys[name_or_power % len(keys)]
        else:
            key = keys[0]
        name, cost, rarity, attack, health = self.creatures[key]
        return CreatureCard(name, cost, rarity, attack, health)

    def create_spell(self, name_or_power: str | int | None = None) -> Card:
        keys = list(self.spells.keys())
        if isinstance(name_or_power, str):
            key = name_or_power.lower()
        elif isinstance(name_or_power, int):
            key = keys[name_or_power % len(keys)]
        else:
            key = keys[0]
        name, cost, rarity, effect_type = self.spells[key]
        return SpellCard(name, cost, rarity, effect_type)

    def create_artifact(self, name_or_power: str | int | None = None) -> Card:
        keys = list(self.artifacts.keys())
        if isinstance(name_or_power, str):
            key = name_or_power.lower()
        elif isinstance(name_or_power, int):
            key = keys[name_or_power % len(keys)]
        else:
            key = keys[0]
        name, cost, rarity, durability, effect = self.artifacts[key]
        return ArtifactCard(name, cost, rarity, durability, effect)

    def create_themed_deck(self, size: int) -> dict[str, Any]:
        deck = Deck()
        if size <= 0:
            return {"deck": deck, "stats": {"total_cards": 0}}

        if not self.deck_order:
            raise ValueError("Deck order is empty.")

        # size is total number of cards in the deck
        # deck_oder is a list of tuples
        # e.g. ("creature", "dragon"), ("spell", "fireball")
        # to create a deck with cyclic looping
        # 0 1 2 3 4 5 6 7 8 9 10 11 12 index
        # 0 1 2 3 4 0 1 2 3 4 0  1  2  index % deck_order(here is 5)
        # 0 1 2 three cards, 3 4 two cards
        for index in range(size):
            category, key = self.deck_order[index % len(self.deck_order)]
            if category == "creature":
                card = self.create_creature(key)
            elif category == "spell":
                card = self.create_spell(key)
            elif category == "artifact":
                card = self.create_artifact(key)
            else:
                raise ValueError(f"Unsupported cycle category: {category}")
            deck.add_card(card)
            random.shuffle(deck.cards)

        return {"deck": deck, "stats": deck.get_deck_stats()}

    def get_supported_types(self) -> dict[str, Any]:
        card_names = []
        for key in self.deck_order:
            if key[0] == "creature":
                card_names.append(key[1])

        spell_names = []
        for key in self.deck_order:
            if key[0] == "spell":
                spell_names.append(key[1])

        artifact_names = []
        for key in self.deck_order:
            if key[0] == "artifact":
                artifact_names.append(key[1])

        return {
            "creatures": card_names,
            "spells": spell_names,
            "artifacts": artifact_names,
        }
