"""
Base class for maze generators.
"""
from abc import ABC, abstractmethod
from typing import Optional, Set, Tuple
import random
from .maze import Maze
from .pattern42 import get_pattern_cells


class MazeGenerator(ABC):
    """
    Base class for all maze generators.
    Handles shared logic like storing dimension and seed and the '42' pattern.
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

    def get_protected_cells(self) -> Set[Tuple[int, int]]:
        """
        Returns the (x, y) coordinates of the '42' pattern.
        """
        return get_pattern_cells(self.width, self.height)
