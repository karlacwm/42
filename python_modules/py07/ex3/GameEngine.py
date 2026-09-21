from typing import Any
from ex0.Card import Card
from ex3.CardFactory import CardFactory
from ex3.GameStrategy import GameStrategy


class GameEngine:
    def __init__(self) -> None:
        self.turns_simulated = 0
        self.total_damage = 0
        self.cards_created = 0
        self.current_hand: list[Card] = []
        self.current_battlefield: list[Any] = []

    def configure_engine(
            self, factory: CardFactory, strategy: GameStrategy) -> None:
        self.factory: CardFactory = factory
        self.strategy: GameStrategy = strategy

    def simulate_turn(self) -> dict[str, Any]:
        if self.strategy is None:
            raise RuntimeError(
                "Engine has not been configured with a strategy.")
        actions = self.strategy.execute_turn(
            hand=self.current_hand,
            battlefield=self.current_battlefield,
        )
        self.turns_simulated += 1
        self.total_damage += int(actions.get("damage_dealt", 0))
        self.cards_created += len(self.current_hand)

        return actions

    def get_engine_status(self) -> dict[str, Any]:
        if self.strategy is None:
            raise RuntimeError(
                "Engine has not been configured with a strategy.")
        return {
            "turns_simulated": self.turns_simulated,
            "strategy_used": self.strategy.get_strategy_name(),
            "total_damage": self.total_damage,
            "cards_created": self.cards_created,
        }
