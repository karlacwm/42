"""Maze generation algorithms."""
from typing import Optional, Set, Tuple
from .maze import Maze
# Import the classes we just made
from .algorithms import PrimGenerator, KruskalGenerator, BacktrackingGenerator


def generate_maze(width: int, height: int,
                  algorithm: str = 'prim',
                  seed: Optional[int] = None,
                  perfect: bool = True,
                  forbidden: Optional[Set[Tuple[int, int]]] = None,
                  loops: int = 0) -> Maze:

    algorithm = algorithm.lower()

    # 1. Select the class
    if algorithm == 'prim':
        generator = PrimGenerator(width, height, seed)
    elif algorithm == 'kruskal':
        generator = KruskalGenerator(width, height, seed)
    elif algorithm == iterative_backtracking:
        generator = BacktrackingGenerator(width, height, seed)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")

    # 2. Run generation (Polymorphism!)
    maze = generator.generate()

    # 3. Handle loops (Post-processing)
    if not perfect and loops > 0:
        if forbidden is None:
            # We can now ask the generator itself for the protected cells!
            forbidden = generator.get_protected_cells()
        maze.add_loops(forbidden, loops)

    return maze
