"""
Maze solver with shortest path detection using BFS.
"""
from typing import List, Tuple, Set, Optional, Any
from collections import deque
from .maze import Maze, Direction


def find_shortest_path(
        maze: Maze,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int
) -> Optional[List[Tuple[int, int]]] | Any:
    """
    Find shortest path from start to end using BFS.
    """
    # Convert to int, handling expression strings
    start_x = int(start_x)
    start_y = int(start_y)

    # Handle expressions like "width - 1"
    if isinstance(end_x, str):
        end_x = eval(
            end_x,
            {"width": maze.width, "height": maze.height}
        )
    else:
        end_x = int(end_x)

    if isinstance(end_y, str):
        end_y = eval(
            end_y,
            {"width": maze.width, "height": maze.height}
        )
    else:
        end_y = int(end_y)

    # Validate coordinates
    if not maze.is_valid(start_x, start_y):
        return None
    if not maze.is_valid(end_x, end_y):
        return None

    # BFS to find shortest path
    queue: deque[Any] = deque([(start_x, start_y, [])])
    visited: Set[Tuple[int, int]] = {(start_x, start_y)}

    while queue:
        x, y, path = queue.popleft()

        # Check if we reached the goal
        if x == end_x and y == end_y:
            return path + [(x, y)]

        # Explore neighbors
        cell = maze.get_cell(x, y)

        for direction in Direction.ALL:
            dx, dy = direction
            nx, ny = x + dx, y + dy

            # Check if neighbor is valid and not visited
            if not maze.is_valid(nx, ny):
                continue
            if (nx, ny) in visited:
                continue

            # Check if there's a wall blocking this direction
            wall = Direction.to_wall(direction)
            if cell.has_wall(wall):
                continue

            visited.add((nx, ny))
            queue.append((nx, ny, path + [(x, y)]))

    return None  # No path found
