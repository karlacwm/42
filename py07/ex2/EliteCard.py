from ex0.Card import Card
from ex2.Combatable import Combatable
from ex2.Magical import Magical
from typing import Any


class EliteCard(Card, Combatable, Magical):
    def __init__(self, name: str, cost: int, rarity: str,
                 attack: int, health: int) -> None:
        super().__init__(name, cost, rarity)
        self.type = "Elite"
        self.attack_damage = attack
        self.health = health
        self.total_mana = 4

    def play(self, game_state: dict) -> dict[str, Any]:
        game_state = {
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": "Elite card entered the battlefield"
        }
        return game_state

    def attack(self, target: Any) -> dict[str, Any]:
        attack_state = {
            "attacker": self.name,
            "target": target,
            "damage": self.attack_damage,
            "combat_type": "melee"
        }
        return attack_state
        
    def defend(self, incoming_damage: int) -> dict[str, Any]:
        damage_blocked = 3
        damage_taken = max(0, incoming_damage - damage_blocked)
        self.health -= damage_taken
        return {
            "defender": self.name, 
            "damage_taken": damage_taken,
            "damage_blocked": damage_blocked, 
            "still_alive": self.health > 0
        }

    def get_combat_stats(self) -> dict[str, Any]:
        return {
            "attack": self.attack_damage, 
            "health": self.health}

    def cast_spell(self, spell_name: str, targets: list) -> dict[str, Any]:
        mana_used = 4
        return {
            "caster": self.name,
            "spell": spell_name,
            "targets": targets,
            "mana_used": mana_used
        }

    def channel_mana(self, amount: int) -> dict[str, Any]:
        self.total_mana += amount
        return {
            "channeled": amount, 
            "total_mana": self.total_mana
        }

    def get_magic_stats(self) -> dict[str, Any]:
        return {"total_mana": self.total_mana}