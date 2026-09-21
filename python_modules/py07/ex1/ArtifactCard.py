from ex0.Card import Card
from typing import Any


class ArtifactCard(Card):
    def __init__(self, name: str, cost: int, rarity: str,
                 durability: int, effect: str) -> None:
        super().__init__(name, cost, rarity)
        self.type = "Artifact"

        if not isinstance(durability, int) or durability < 0:
            raise ValueError("Durability must be a non-negative integer.")

        self.durability = durability
        self.effect = effect

    def play(self, game_state: dict[str, Any]) -> dict[str, Any]:
        game_state = {
            'card_played': self.name,
            'mana_used': self.cost,
            'effect': f'Permanent: {self.effect}'
        }
        return game_state

    def activate_ability(self) -> dict[str, Any]:
        self.durability -= 1
        return {
            'ability_activated': self.effect,
            'durability_remaining': self.durability
        }
