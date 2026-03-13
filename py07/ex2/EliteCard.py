from ex0.Card import Card
from ex2 import Combatable, Magical
from typing import Any


class EliteCard(Card, Combatable, Magical):
    def __init__(self, name: str, cost: int, rarity: str,
                 attack: int, health: int) -> None:
        super().__init__(name, cost, rarity)
        self.type = "Elite"
        self.attack = attack
        self.health = health
        self.total_mana = 4

    def play(self, game_state: dict) -> dict[str, Any]:
        game_state = {
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": "Elite card entered the battlefield"
        }
        return game_state

    def attack(self, target) -> dict[str, Any]:
        return {
            'attacker': self.name,
            'target': target,
            'damage': self.attack,
            'combat_type': 'melee'
        }

    def cast_spell(self, spell_name: str, targets: list) -> dict[str, Any]:
        mana_used = 4
        return {
            'caster': self.name,
            'spell': spell_name,
            'targets': targets,
            'mana_used': mana_used
        }
