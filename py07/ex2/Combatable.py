from abc import ABC, abstractmethod
from typing import Any


class Combatable(ABC):
    @abstractmethod
    def attack(self, target) -> dict[str, Any]:
        pass

    @abstractmethod
    def defend(self, incoming_damage: int) -> dict[str, Any]:
        pass

    @abstractmethod
    def get_combat_stats(self) -> dict[str, Any]:
        pass
