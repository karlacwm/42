"""Maze generation algorithms."""
import random
from typing import Optional, List, Tuple, Set
from .maze import Maze
from .iterative_backtracking import generate_iterative_backtracking


class UnionFind:
    """Union-Find (Disjoint Set) data structure for Kruskal's algorithm."""

    def __init__(self, size: int) -> None:
        """Initialize Union-Find structure."""
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, x: int) -> int:
        """Find the root of element x with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """
        Union two sets.

        Returns:
            True if sets were merged, False if already in same set
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        return True


def generate_prim(width: int, height: int, seed: Optional[int] = None) -> Maze:
    """
    Generate a perfect maze using Prim's algorithm.

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

    # Start with a random cell
    start_x = random.randint(0, width - 1)
    start_y = random.randint(0, height - 1)

    visited: Set[Tuple[int, int]] = {(start_x, start_y)}
    walls: List[Tuple[int, int, int, int]] = []

    # Add walls of starting cell
    for nx, ny, direction in maze.get_neighbors(start_x, start_y):
        walls.append((start_x, start_y, nx, ny))

    # Process walls
    while walls:
        # Pick a random wall
        wall_idx = random.randint(0, len(walls) - 1)
        x1, y1, x2, y2 = walls.pop(wall_idx)

        # If only one of the cells is visited, remove the wall
        if (x2, y2) not in visited:
            maze.remove_wall_between(x1, y1, x2, y2)
            visited.add((x2, y2))

            # Add walls of the newly visited cell
            for nx, ny, direction in maze.get_neighbors(x2, y2):
                if (nx, ny) not in visited:
                    walls.append((x2, y2, nx, ny))

    return maze


def generate_kruskal(width: int, height: int, seed: Optional[int] = None) -> Maze:
    """
    Generate a perfect maze using Kruskal's algorithm.

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

    # Create list of all possible walls between cells
    edges: List[Tuple[int, int, int, int]] = []
    for y in range(height):
        for x in range(width):
            # Add east wall if not on right edge
            if x < width - 1 and maze.is_valid(x, y) and maze.is_valid(x + 1, y):
                edges.append((x, y, x + 1, y))
            # Add south wall if not on bottom edge
            if y < height - 1 and maze.is_valid(x, y) and maze.is_valid(x, y + 1):
                edges.append((x, y, x, y + 1))

    # Shuffle edges
    random.shuffle(edges)

    # Create Union-Find structure
    # Map each cell to an index
    def cell_index(x: int, y: int) -> int:
        return y * width + x

    uf = UnionFind(width * height)

    # Process edges
    for x1, y1, x2, y2 in edges:
        idx1 = cell_index(x1, y1)
        idx2 = cell_index(x2, y2)

        # If cells are in different sets, remove wall and union them
        if uf.union(idx1, idx2):
            maze.remove_wall_between(x1, y1, x2, y2)
        else:
            pass

    return maze


def generate_maze(width: int, height: int,
                  algorithm: str = 'prim',
                  seed: Optional[int] = None) -> Maze:
    """
    Generate a perfect maze using the specified algorithm.

    Args:
        width: Width of the maze
        height: Height of the maze
        algorithm: Algorithm to use ('prim', 'kruskal', or 'iterative_backtracking')
        seed: Random seed for reproducibility

    Returns:
        Generated maze

    Raises:
        ValueError: If algorithm is not supported
    """
    algorithm = algorithm.lower()

    if algorithm == 'prim':
        return generate_prim(width, height, seed)
    elif algorithm == 'kruskal':
        return generate_kruskal(width, height, seed)
    elif algorithm == 'iterative_backtracking':
        return generate_iterative_backtracking(width, height, seed)
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
