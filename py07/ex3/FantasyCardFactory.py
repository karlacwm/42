from typing import Any

from ex0 import Card, CreatureCard
from ex1 import ArtifactCard, Deck, SpellCard
from ex3.CardFactory import CardFactory


class FantasyCardFactory(CardFactory):
    def __init__(
        self,
        cards: dict[str, tuple[str, int, str, int, int]],
        spells: dict[str, tuple[str, int, str, str]],
        artifacts: dict[str, tuple[str, int, str, int, str]],
        deck_order: list[tuple[str, str]],
    ) -> None:
        self.cards = cards
        self.spells = spells
        self.artifacts = artifacts
        self.deck_order = deck_order

    def create_creature(self, name_or_power: str | int | None = None) -> Card:
        keys = list(self.cards.keys())
        if isinstance(name_or_power, str):
            key = name_or_power.lower()
        elif isinstance(name_or_power, int):
            key = keys[name_or_power % len(keys)]
        else:
            key = keys[0]
        name, cost, rarity, attack, health = self.cards[key]
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
        if size <= 0:
            return {"deck": Deck(), "stats": {"total_cards": 0}}

        if not self.deck_order:
            raise ValueError("Deck order is empty.")

        deck = Deck()
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

        return {"deck": deck, "stats": deck.get_deck_stats()}

    def get_supported_types(self) -> dict[str, Any]:
        card_names = []
        for key in self.cards:
            card_names.append(key)

        spell_names = []
        for key in self.spells:
            spell_names.append(key)

        artifact_names = []
        for key in self.artifacts:
            artifact_names.append(key)

        return {
            "creatures": card_names,
            "spells": spell_names,
            "artifacts": artifact_names,
        }
