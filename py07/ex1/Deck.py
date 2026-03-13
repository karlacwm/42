from ex0.Card import Card
from typing import Any
import random


class Deck:
    def __init__(self) -> None:
        self.cards: list[Card] = []

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def remove_card(self, card_name: str) -> bool:
        for card in self.cards:
            if card.name == card_name:
                self.cards.remove(card)
                return True
        return False

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def draw_card(self) -> Card | None:
        if self.cards:
            return self.cards.pop(0)
        return None

    def get_deck_stats(self) -> dict[str, Any]:
        creature_count = 0
        spell_count = 0
        artifact_count = 0
        for card in self.cards:
            if card.type == "Creature":
                creature_count += 1
            elif card.type == "Spell":
                spell_count += 1
            elif card.type == "Artifact":
                artifact_count += 1

        total_cost = 0
        avg_cost = 0.0
        if self.cards:
            for card in self.cards:
                total_cost += card.cost
            avg_cost = total_cost / len(self.cards)

        return {
            "total_cards": len(self.cards),
            "creatures": creature_count,
            "spells": spell_count,
            "artifacts": artifact_count,
            "avg_cost": round(avg_cost, 1)
        }
