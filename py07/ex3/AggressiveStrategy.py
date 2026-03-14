from typing import Any
from ex3.GameStrategy import GameStrategy


class AggressiveStrategy(GameStrategy):
    def __init__(self, mana_limit: int, spell_damage: dict[str, int],
        enemy_tag: str, default_targets: list[str]) -> None:
        self.mana_limit = mana_limit
        self.spell_damage = spell_damage
        self.enemy_tag = enemy_tag
        self.default_targets = default_targets

    def execute_turn(self, hand: list, battlefield: list) -> dict[str, Any]:
        unit_cards = []
        other_cards = []
        for card in hand:
            if getattr(card, "type", "") == "Creature":
                unit_cards.append(card)
            else:
                other_cards.append(card)

        for index in range(len(unit_cards)):
            for second_index in range(index + 1, len(unit_cards)):
                if unit_cards[index].cost > unit_cards[second_index].cost:
                    temp = unit_cards[index]
                    unit_cards[index] = unit_cards[second_index]
                    unit_cards[second_index] = temp

        for index in range(len(other_cards)):
            for second_index in range(index + 1, len(other_cards)):
                if other_cards[index].cost > other_cards[second_index].cost:
                    temp = other_cards[index]
                    other_cards[index] = other_cards[second_index]
                    other_cards[second_index] = temp

        ordered_cards = []
        for card in unit_cards:
            ordered_cards.append(card)
        for card in other_cards:
            ordered_cards.append(card)

        played_cards: list[Any] = []
        mana_used = 0
        for card in ordered_cards:
            if mana_used + card.cost <= self.mana_limit:
                played_cards.append(card)
                mana_used += card.cost

        cards_played = []
        for card in played_cards:
            cards_played.append(card.name)

        target_list = self.prioritize_targets(battlefield)

        unit_damage = 0
        spell_damage = 0
        for card in played_cards:
            if getattr(card, "type", "") == "Creature":
                unit_damage += getattr(card, "attack", 0)
            if getattr(card, "type", "") == "Spell":
                spell_damage += self.spell_damage.get(card.name, 0)

        damage_dealt = (unit_damage + spell_damage) if target_list else 0

        return {
            "cards_played": cards_played,
            "mana_used": mana_used,
            "targets_attacked": target_list,
            "damage_dealt": damage_dealt
        }

    def get_strategy_name(self) -> str:
        return "AggressiveStrategy"

    def prioritize_targets(self, available_targets: list) -> list:
        targets = []
        for target in available_targets:
            if self.enemy_tag in str(target):
                targets.append(target)
        if targets:
            return targets
        return self.default_targets