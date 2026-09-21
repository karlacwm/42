from typing import Any
from ex0.Card import Card
from ex3.GameStrategy import GameStrategy


class AggressiveStrategy(GameStrategy):
    def __init__(self, mana_limit: int, spell_damage: dict[str, int],
                 enemy_tag: str, default_targets: list[str]) -> None:
        self.mana_limit = mana_limit
        self.spell_damage = spell_damage
        self.enemy_tag = enemy_tag
        self.default_targets = default_targets

    def execute_turn(
            self, hand: list[Card], battlefield: list[Any]) -> dict[str, Any]:
        # agressive strategy: damage and low cost cards first
        # only creatures have attack power, so creature cards are prioritized
        creature_cards = []
        other_cards = []
        for card in hand:
            if getattr(card, "type", "") == "Creature":
                creature_cards.append(card)
            else:
                other_cards.append(card)

        for i in range(len(creature_cards)):
            for j in range(i + 1, len(creature_cards)):
                if creature_cards[i].cost > creature_cards[j].cost:
                    temp = creature_cards[i]
                    creature_cards[i] = creature_cards[j]
                    creature_cards[j] = temp
        for i in range(len(other_cards)):
            for j in range(i + 1, len(other_cards)):
                if other_cards[i].cost > other_cards[j].cost:
                    temp = other_cards[i]
                    other_cards[i] = other_cards[j]
                    other_cards[j] = temp

        ordered_cards = []
        for card in creature_cards:
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

        target_list = self.prioritize_targets(available_targets=battlefield)

        attack_damage = 0
        spell_damage = 0
        for card in played_cards:
            if card.type == "Creature":
                attack_damage += card.attack
            elif card.type == "Spell":
                spell_damage += self.spell_damage.get(card.name, 0)

        damage_dealt = (attack_damage + spell_damage) if target_list else 0

        return {
            "cards_played": cards_played,
            "mana_used": mana_used,
            "targets_attacked": target_list,
            "damage_dealt": damage_dealt
        }

    def get_strategy_name(self) -> str:
        return "AggressiveStrategy"

    def prioritize_targets(self, available_targets: list[Any]) -> list[Any]:
        targets = []
        for target in available_targets:
            if self.enemy_tag in str(target):
                targets.append(target)
        if targets:
            return targets
        return self.default_targets
