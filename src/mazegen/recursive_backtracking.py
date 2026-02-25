"""Recursive backtracking maze generation algorithm."""
import random
from typing import Optional, Set, List, Tuple
from .maze import Maze


def generate_recursive_backtracking(width: int, height: int, seed: Optional[int] = None) -> Maze:
    """
    Generate a perfect maze using the Recursive Backtracking algorithm.

    The algorithm works by:
    1. Starting at a random cell
    2. Marking it as visited
    3. Randomly choosing an unvisited neighbor
    4. Removing the wall between current and chosen neighbor
    5. Moving to the neighbor and repeating
    6. When all neighbors are visited, backtracking to the previous cell
    7. Continuing until the stack is empty

    Args:
        width: Width of the maze
        height: Height of the maze
        seed: Random seed for reproducibility

    Returns:
        Generated maze
    """
    if seed is not None:
        random.seed(seed)

    maze = Maze(width, height)
    visited: Set[Tuple[int, int]] = set()
    stack: List[Tuple[int, int]] = []

    # Start with a random cell
    start_x = random.randint(0, width - 1)
    start_y = random.randint(0, height - 1)

    stack.append((start_x, start_y))
    visited.add((start_x, start_y))

    # Main loop: process cells from the stack
    while stack:
        current_x, current_y = stack[-1]

        # Get all unvisited neighbors
        unvisited_neighbors = [
            (nx, ny, direction)
            for nx, ny, direction in maze.get_neighbors(current_x, current_y)
            if (nx, ny) not in visited
        ]

        if not unvisited_neighbors:
            # No unvisited neighbors, backtrack
            stack.pop()
        else:
            # Choose a random unvisited neighbor
            next_x, next_y, direction = random.choice(unvisited_neighbors)

            # Remove wall between current and next cell
            maze.remove_wall_between(current_x, current_y, next_x, next_y)

            # Mark next cell as visited and push to stack
            visited.add((next_x, next_y))
            stack.append((next_x, next_y))

    return maze
