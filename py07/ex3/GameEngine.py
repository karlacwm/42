from typing import Any
from ex3.CardFactory import CardFactory
from ex3.GameStrategy import GameStrategy


class GameEngine:
    def __init__(self) -> None:
        self.factory: CardFactory | None = None
        self.strategy: GameStrategy | None = None
        self.turns_simulated = 0
        self.total_damage = 0
        self.cards_created = 0
        self.current_hand: list[Any] = []
        self.current_battlefield: list[str] = []

    def configure_engine(self, factory: CardFactory, strategy: GameStrategy) -> None:
        self.factory = factory
        self.strategy = strategy

    def simulate_turn(self) -> dict[str, Any]:
        actions = self.strategy.execute_turn(
            self.current_hand,
            self.current_battlefield,
        )
        self.turns_simulated += 1
        self.total_damage += int(actions.get("damage_dealt", 0))
        self.cards_created += len(self.current_hand)

        return actions

    def get_engine_status(self) -> dict[str, Any]:
        return {
            "turns_simulated": self.turns_simulated,
            "strategy_used": self.strategy.get_strategy_name(),
            "total_damage": self.total_damage,
            "cards_created": self.cards_created,
        }
