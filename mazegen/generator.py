"""Factory for creating maze generators."""
from typing import Optional, Set, Tuple
from .maze import Maze
from .class_maze_generator import MazeGenerator
from .algorithms import PrimGenerator, KruskalGenerator, BacktrackingGenerator


def generate_maze(width: int, height: int,
                  algorithm: str = 'prim',
                  seed: Optional[int] = None,
                  perfect: bool = True,
                  forbidden: Optional[Set[Tuple[int, int]]] = None,
                  loops: int = 0) -> Maze:
    """
    Factory function to generate a maze using the specified algorithm.
    """
    algorithm = algorithm.lower()
    generator: MazeGenerator

    if algorithm == 'prim':
        generator = PrimGenerator(width, height, seed)
    elif algorithm == 'kruskal':
        generator = KruskalGenerator(width, height, seed)
    elif algorithm == 'iterative_backtracking':
        generator = BacktrackingGenerator(width, height, seed)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")

    maze = generator.generate()

    if not perfect and loops > 0:
        if forbidden is None:
            forbidden = generator.get_protected_cells()
        maze.add_loops(forbidden, loops)
    return maze
