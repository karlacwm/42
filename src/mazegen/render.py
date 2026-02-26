"""Rendering utilities for mazes."""
import sys
import time
from typing import List, Tuple, Set
from .maze import Maze, Wall
from .render_color import colorize_token, get_maze_color_from_config
# from .config import parse_config  # still used for validation if needed


def get_pattern_cells(width: int, height: int) -> Set[Tuple[int, int]]:
    """Generates (x, y) coordinates for '42' in the center."""

    cx, cy = width // 2, height // 2

    digit_4 = {
        (0, 0), (0, 1), (0, 2),
        (1, 2),
        (2, 2), (2, 3), (2, 4)
    }
    digit_2 = {
        (0, 0), (1, 0), (2, 0),
        (2, 1),
        (0, 2), (1, 2), (2, 2),
        (0, 3),
        (0, 4), (1, 4), (2, 4)
    }

    start_x = cx - 3
    start_y = cy - 2

    pattern = set()

    for dx, dy in digit_4:
        pattern.add((start_x + dx, start_y + dy))
    for dx, dy in digit_2:
        pattern.add((start_x + 4 + dx, start_y + dy))

    return pattern


def _build_wall_grids(
        maze: Maze
) -> Tuple[List[List[bool]], List[List[bool]], int, int]:
    width = maze.width
    height = maze.height

    render_w = width * 2 + 1
    render_h = height * 2 + 1

    # Precompute wall grid
    vertical = [[False] * render_w for _ in range(render_h)]
    horizontal = [[False] * render_w for _ in range(render_h)]

    # Fill walls from maze cells
    for y in range(height):
        for x in range(width):
            cell = maze.get_cell(x, y)

            rx = x * 2 + 1
            ry = y * 2 + 1

            # WEST wall (left border)
            if x == 0 and cell.has_wall(Wall.WEST):
                vertical[ry][rx - 1] = True

            # NORTH wall (top border)
            if y == 0 and cell.has_wall(Wall.NORTH):
                horizontal[ry - 1][rx] = True

            # EAST wall
            if cell.has_wall(Wall.EAST):
                vertical[ry][rx + 1] = True

            # SOUTH wall
            if cell.has_wall(Wall.SOUTH):
                horizontal[ry + 1][rx] = True

    return vertical, horizontal, render_w, render_h


def render_unicode(
        maze: Maze, delay: float = 0.01,
        config_path: str = "config.txt"
) -> str:
    width, height = maze.width, maze.height
    # load and validate configuration; helper returns an RGB tuple
    maze_color = get_maze_color_from_config(config_path, "maze")
    egg_color = get_maze_color_from_config(config_path, "egg")
    wall_color = get_maze_color_from_config(config_path, "wall")
    vertical, horizontal, render_w, render_h = _build_wall_grids(maze)
    pattern = get_pattern_cells(width, height)

    # Standard intersection map
    wall_unicode = {
        (True, True, True, True): "╬",
        (True, False, True, True): "╣",
        (True, True, True, False): "╠",
        (True, True, False, True): "╩",
        (False, True, True, True): "╦",
        (True, False, True, False): "║",
        (False, True, False, True): "═",
        (True, False, False, True): "╝",
        (True, True, False, False): "╚",
        (False, False, True, True): "╗",
        (False, True, True, False): "╔",
    }

    lines = []
    for ry in range(render_h):
        line = ""
        for rx in range(render_w):
            # Map render coordinates to the logical cell (cx, cy)
            # We use distinct logic for "on the line" vs "inside the cell"
            cx = rx // 2
            cy = ry // 2

            # Check if current/adjacent cells are in the pattern
            curr_in_pat = (cx, cy) in pattern
            left_in_pat = (cx - 1, cy) in pattern if rx > 0 else False
            up_in_pat = (cx, cy - 1) in pattern if ry > 0 else False
            diag_in_pat = (
                (cx - 1, cy - 1) in pattern
                if (rx > 0 and ry > 0) else False
            )

            token = ""

            # --- A: Intersections (Corners) ---
            if ry % 2 == 0 and rx % 2 == 0:
                # If any of the 4 surrounding cells is a pattern cell,
                # we recalculate the intersection to ensure a "box" look.
                is_pat_corner = (
                    curr_in_pat or left_in_pat or
                    up_in_pat or diag_in_pat
                )

                up = ry > 0 and vertical[ry - 1][rx]
                down = ry < render_h - 1 and vertical[ry + 1][rx]
                left = rx > 0 and horizontal[ry][rx - 1]
                right = rx < render_w - 1 and horizontal[ry][rx + 1]

                # Override: If it's a pattern corner,
                # force the connections
                if is_pat_corner:
                    # Logic: If I'm the Top-Left of a pattern cell,
                    # I need Right and Down.
                    # This builds the box connections.
                    u = up or (up_in_pat or diag_in_pat)
                    d = down or (curr_in_pat or left_in_pat)
                    ll = left or (left_in_pat or diag_in_pat)
                    r = right or (curr_in_pat or up_in_pat)
                    token = wall_unicode.get((u, r, d, ll), "░")
                else:
                    token = wall_unicode.get((up, right, down, left), "░")

            # --- B: Horizontal segments ---
            elif ry % 2 == 0 and rx % 2 == 1:
                # Force wall if cell above or below is a pattern cell
                if curr_in_pat or up_in_pat:
                    token = "═══"  # Adjust to 3 wide to fit the ╔═══╗ request
                else:
                    token = "═══" if horizontal[ry][rx] else "░░░"

            # --- C: Vertical segments ---
            elif ry % 2 == 1 and rx % 2 == 0:
                # Force wall if cell left or right is a pattern cell
                if curr_in_pat or left_in_pat:
                    token = "║"
                else:
                    token = "║" if vertical[ry][rx] else "░"

            # --- D: Cell Interior ---
            else:
                token = "███" if curr_in_pat else "░░░"

            if token == "███":
                colored = colorize_token(token, egg_color)
            elif token == "░░░" or token == "░":
                colored = colorize_token(token, maze_color)
            else:
                colored = colorize_token(token, wall_color)
            line += colored
            sys.stdout.write(colored)
            sys.stdout.flush()
            time.sleep(delay)

        lines.append(line)
        sys.stdout.write("\n")

    return "\n".join(lines)


def render_unicode_with_path(
        maze: Maze,
        path: List[Tuple[int, int]],
        delay: float = 0.01,
        config_path: str = "config.txt"
) -> str:
    """
    Render maze with the shortest path highlighted.

    Args:
        maze: The maze to render
        path: List of (x, y) coordinates representing path
        delay: Delay between rendering each token
        config_path: Path to configuration file

    Returns:
        Rendered maze as string with path highlighted
    """
    width, height = maze.width, maze.height
    maze_color = get_maze_color_from_config(
        config_path, "maze"
    )
    egg_color = get_maze_color_from_config(config_path, "egg")
    wall_color = get_maze_color_from_config(
        config_path, "wall"
    )
    path_color = get_maze_color_from_config(
        config_path, "path"
    )
    vertical, horizontal, render_w, render_h = (
        _build_wall_grids(maze)
    )
    pattern = get_pattern_cells(width, height)

    # Convert path to a set for O(1) lookup
    path_set: Set[Tuple[int, int]] = set(path)

    # Standard intersection map
    wall_unicode = {
        (True, True, True, True): "╬",
        (True, False, True, True): "╣",
        (True, True, True, False): "╠",
        (True, True, False, True): "╩",
        (False, True, True, True): "╦",
        (True, False, True, False): "║",
        (False, True, False, True): "═",
        (True, False, False, True): "╝",
        (True, True, False, False): "╚",
        (False, False, True, True): "╗",
        (False, True, True, False): "╔",
    }

    lines = []
    for ry in range(render_h):
        line = ""
        for rx in range(render_w):
            cx = rx // 2
            cy = ry // 2

            # Check if current/adjacent cells are in pattern
            curr_in_pat = (cx, cy) in pattern
            left_in_pat = (
                (cx - 1, cy) in pattern if rx > 0 else False
            )
            up_in_pat = (
                (cx, cy - 1) in pattern if ry > 0 else False
            )
            diag_in_pat = (
                (cx - 1, cy - 1) in pattern
                if (rx > 0 and ry > 0) else False
            )

            # Check if current cell is on path
            on_path = (cx, cy) in path_set

            token = ""

            # --- A: Intersections (Corners) ---
            if ry % 2 == 0 and rx % 2 == 0:
                is_pat_corner = (
                    curr_in_pat or left_in_pat or
                    up_in_pat or diag_in_pat
                )

                up = ry > 0 and vertical[ry - 1][rx]
                down = (
                    ry < render_h - 1 and vertical[ry + 1][rx]
                )
                left = rx > 0 and horizontal[ry][rx - 1]
                right = (
                    rx < render_w - 1 and
                    horizontal[ry][rx + 1]
                )

                if is_pat_corner:
                    u = up or (up_in_pat or diag_in_pat)
                    d = down or (
                        curr_in_pat or left_in_pat
                    )
                    ll = left or (
                        left_in_pat or diag_in_pat
                    )
                    r = right or (
                        curr_in_pat or up_in_pat
                    )
                    token = wall_unicode.get(
                        (u, r, d, ll), "░"
                    )
                else:
                    token = wall_unicode.get(
                        (up, right, down, left), "░"
                    )

            # --- B: Horizontal segments ---
            elif ry % 2 == 0 and rx % 2 == 1:
                if curr_in_pat or up_in_pat:
                    token = "═══"
                else:
                    token = (
                        "═══" if horizontal[ry][rx]
                        else "░░░"
                    )

            # --- C: Vertical segments ---
            elif ry % 2 == 1 and rx % 2 == 0:
                if curr_in_pat or left_in_pat:
                    token = "║"
                else:
                    token = (
                        "║" if vertical[ry][rx] else "░"
                    )

            # --- D: Cell Interior ---
            else:
                if curr_in_pat:
                    token = "███"
                elif on_path:
                    token = "···"
                else:
                    token = "░░░"

            # Colorize based on content
            if token == "███":
                colored = colorize_token(token, egg_color)
            elif token == "···":
                colored = colorize_token(
                    token, path_color
                )
            elif token == "░░░" or token == "░":
                colored = colorize_token(token, maze_color)
            else:
                colored = colorize_token(
                    token, wall_color
                )
            line += colored
            sys.stdout.write(colored)
            sys.stdout.flush()
            time.sleep(delay)

        lines.append(line)
        sys.stdout.write("\n")

    return "\n".join(lines)

