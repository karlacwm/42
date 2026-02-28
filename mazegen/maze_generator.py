from abc import ABC, abstractmethod
from typing import Optional, Set, Tuple
import random
from .maze import Maze


class MazeGenerator(ABC):
    """
    Base class for all maze generators.
    Handles shared logic like seeding and the '42' pattern.
    """
    def __init__(self, width: int, height: int, seed: Optional[int] = None) -> None:
        self.width = width
        self.height = height
        self.seed = seed
        if seed is not None:
            random.seed(seed)

    @abstractmethod
    def generate(self) -> Maze:
        """Subclasses must implement this to return a Maze."""
        pass

    def _get_protected_cells(self) -> Set[Tuple[int, int]]:
        """
        Returns the (x, y) coordinates of the '42' pattern.
        """
        # 1. Size Check
        if self.width < 12 or self.height < 10:
            return set()

        coords = set()
        cx, cy = self.width // 2, self.height // 2

        # 2. Pattern Offsets (The exact same logic you had before)
        pattern_offsets = [
            # Number 4
            (-4, -2), (-2, -2), (-4, -1), (-2, -1),
            (-4,  0), (-3, 0), (-2, 0), (-2, 1), (-2, 2),
            # Number 2
            (1, -2), (2, -2), (3, -2), (3, -1),
            (1,  0), (2,  0), (3,  0), (1,  1),
            (1,  2), (2,  2), (3,  2)
        ]

        for dx, dy in pattern_offsets:
            coords.add((cx + dx, cy + dy))

        return coords
