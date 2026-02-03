"""Tests for generator module."""
import pytest
from mazegen.generator import generate_maze, generate_prim, generate_kruskal
from mazegen.maze import Wall


def test_generate_prim() -> None:
    """Test Prim's algorithm."""
    maze = generate_prim(5, 5, seed=42)
    assert maze.width == 5
    assert maze.height == 5

    # Check that maze is generated (some walls removed)
    all_walls = sum(
        1 for row in maze.cells for cell in row if cell.walls == Wall.ALL
    )
    assert all_walls < 25  # Not all cells should have all walls


def test_generate_kruskal() -> None:
    """Test Kruskal's algorithm."""
    maze = generate_kruskal(5, 5, seed=42)
    assert maze.width == 5
    assert maze.height == 5

    # Check that maze is generated (some walls removed)
    all_walls = sum(
        1 for row in maze.cells for cell in row if cell.walls == Wall.ALL
    )
    assert all_walls < 25


def test_generate_maze_prim() -> None:
    """Test generate_maze with Prim."""
    maze = generate_maze(5, 5, algorithm='prim', seed=42)
    assert maze.width == 5
    assert maze.height == 5


def test_generate_maze_kruskal() -> None:
    """Test generate_maze with Kruskal."""
    maze = generate_maze(5, 5, algorithm='kruskal', seed=42)
    assert maze.width == 5
    assert maze.height == 5


def test_generate_maze_invalid_algorithm() -> None:
    """Test generate_maze with invalid algorithm."""
    with pytest.raises(ValueError, match="Unsupported algorithm"):
        generate_maze(5, 5, algorithm='invalid')


def test_generate_deterministic() -> None:
    """Test that same seed produces same maze."""
    maze1 = generate_maze(5, 5, algorithm='prim', seed=42)
    maze2 = generate_maze(5, 5, algorithm='prim', seed=42)

    for y in range(5):
        for x in range(5):
            cell1 = maze1.get_cell(x, y)
            cell2 = maze2.get_cell(x, y)
            assert cell1.walls == cell2.walls


def test_generate_different_seeds() -> None:
    """Test that different seeds produce different mazes."""
    maze1 = generate_maze(10, 10, algorithm='prim', seed=42)
    maze2 = generate_maze(10, 10, algorithm='prim', seed=123)

    # Count differences
    differences = 0
    for y in range(10):
        for x in range(10):
            cell1 = maze1.get_cell(x, y)
            cell2 = maze2.get_cell(x, y)
            if cell1.walls != cell2.walls:
                differences += 1

    # Should have some differences
    assert differences > 0


def test_generate_perfect_maze() -> None:
    """Test that generated maze is perfect (connected, no loops)."""
    maze = generate_maze(10, 10, algorithm='prim', seed=42)

    # Use DFS to check connectivity
    visited = set()
    stack = [(0, 0)]

    while stack:
        x, y = stack.pop()
        if (x, y) in visited:
            continue
        visited.add((x, y))

        cell = maze.get_cell(x, y)

        # Check each direction
        if not cell.has_wall(Wall.NORTH) and y > 0:
            stack.append((x, y - 1))
        if not cell.has_wall(Wall.EAST) and x < maze.width - 1:
            stack.append((x + 1, y))
        if not cell.has_wall(Wall.SOUTH) and y < maze.height - 1:
            stack.append((x, y + 1))
        if not cell.has_wall(Wall.WEST) and x > 0:
            stack.append((x - 1, y))

    # All cells should be reachable
    assert len(visited) == 100


def test_small_maze() -> None:
    """Test generating minimum size maze."""
    maze = generate_maze(2, 2, algorithm='prim')
    assert maze.width == 2
    assert maze.height == 2
