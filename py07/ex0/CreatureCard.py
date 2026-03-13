from .Card import Card
from typing import Any


class CreatureCard(Card):
    def __init__(self, name: str, cost: int, rarity: str,
                 attack: int, health: int) -> None:
        super().__init__(name, cost, rarity)
        self.type = "Creature"

        if not isinstance(attack, int) or attack < 0:
            raise ValueError("Attack must be a positive integer.")
        if not isinstance(health, int) or health < 0:
            raise ValueError("Health must be a positive integer.")

        self.attack = attack
        self.health = health

    def play(self, game_state: dict[str, Any]) -> dict[str, Any]:
        game_state = {
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": "Creature summoned to battlefield"
        }
        return game_state

    def attack_target(self, target: Any) -> dict[str, Any]:
        attack_state: dict[str, Any] = {
            "attacker": self.name,
            "target": target,
            "damage_dealt": self.attack,
            "combat_resolved": True
        }
        return attack_state

    def get_card_info(self) -> dict[str, Any]:
        info: dict[str, Any] = super().get_card_info()
        info["attack"] = self.attack
        info["health"] = self.health
        return info
