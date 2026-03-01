"""Rendering functions for mazes."""
import sys
import time
import os
from typing import List, Tuple, Set
from .maze import Maze, Wall
from .render_colour import colourize_token, get_maze_colour_from_config
from .pattern42 import get_pattern_cells
from .config import parse_config


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


def _build_wall_grids(
        maze: Maze
) -> Tuple[List[List[bool]], List[List[bool]], int, int]:
    """
    Helper to create boolean grids for vertical and horizontal walls.
    """
    render_w = maze.width * 2 + 1
    render_h = maze.height * 2 + 1

    # Precompute wall grid
    vertical = [[False] * render_w for _ in range(render_h)]
    horizontal = [[False] * render_w for _ in range(render_h)]

    # Fill walls from maze cells
    for y in range(maze.height):
        for x in range(maze.width):
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
    """
    Render the maze using Unicode block characters.
    """
    width, height = maze.width, maze.height

    # Load colours
    maze_colour = get_maze_colour_from_config(config_path, "maze")
    egg_colour = get_maze_colour_from_config(config_path, "egg")
    wall_colour = get_maze_colour_from_config(config_path, "wall")
    entry_colour = get_maze_colour_from_config(config_path, "entry")
    exit_colour = get_maze_colour_from_config(config_path, "exit")

    # Get entry and exit coord from config
    cfg = parse_config(config_path)
    entry_x = cfg.get('entry_x')
    entry_y = cfg.get('entry_y')
    exit_x = cfg.get('exit_x')
    exit_y = cfg.get('exit_y')
    if isinstance(exit_x, str):
        exit_x = eval(exit_x, {"width": width, "height": height})
    if isinstance(exit_y, str):
        exit_y = eval(exit_y, {"width": width, "height": height})

    vertical, horizontal, render_w, render_h = (_build_wall_grids(maze))
    pattern = get_pattern_cells(width, height)

    lines = []
    for ry in range(render_h):
        line = ""
        for rx in range(render_w):
            cx = rx // 2
            cy = ry // 2

            curr_in_pat = (cx, cy) in pattern
            left_in_pat = (cx - 1, cy) in pattern if rx > 0 else False
            up_in_pat = (cx, cy - 1) in pattern if ry > 0 else False
            diag_in_pat = (
                (cx - 1, cy - 1) in pattern if (rx > 0 and ry > 0) else False
            )

            token = ""
            # Intersections (Corners)
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

                # Override: If it's a pattern corner, force the connections
                if is_pat_corner:
                    # Logic: If i'm the top-left of a pattern cell,
                    # i need right and down. This builds the box connections.
                    u = up or (up_in_pat or diag_in_pat)
                    d = down or (curr_in_pat or left_in_pat)
                    ll = left or (left_in_pat or diag_in_pat)
                    r = right or (curr_in_pat or up_in_pat)
                    token = wall_unicode.get((u, r, d, ll), "░")
                else:
                    token = wall_unicode.get((up, right, down, left), "░")

            # Horizontal segments
            elif ry % 2 == 0 and rx % 2 == 1:
                # Force wall if cell above or below is a pattern cell
                if curr_in_pat or up_in_pat:
                    token = "═══"
                else:
                    token = "═══" if horizontal[ry][rx] else "░░░"

            # Vertical segments
            elif ry % 2 == 1 and rx % 2 == 0:
                # Force wall if cell left or right is a pattern cell
                if curr_in_pat or left_in_pat:
                    token = "║"
                else:
                    token = "║" if vertical[ry][rx] else "░"

            # Cell Interior
            else:
                token = "███" if curr_in_pat else "░░░"

            # Colourize based on content and position
            is_entry = (cx == entry_x and cy == entry_y)
            is_exit = (cx == exit_x and cy == exit_y)
            is_cell_interior = (ry % 2 == 1 and rx % 2 == 1)

            if token == "███":
                coloured = colourize_token(token, egg_colour)
            elif is_entry and (token == "░░░" or token == "░"):
                coloured = colourize_token(token, entry_colour)
            elif is_exit and token == "░░░" and is_cell_interior:
                coloured = colourize_token(token, exit_colour)
            elif token == "░░░" or token == "░":
                coloured = colourize_token(token, maze_colour)
            else:
                coloured = colourize_token(token, wall_colour)
            line += coloured
            sys.stdout.write(coloured)
            sys.stdout.flush()
            time.sleep(delay)

        lines.append(line)
        sys.stdout.write("\n")

    return "\n".join(lines)


def render_path_animation(
        maze: Maze,
        path: List[Tuple[int, int]],
        config_path: str = "config.txt",
        cell_delay: float = 0.05,
        wall_delay: float = 0.03
) -> None:
    """
    Animate path discovery cell by cell, then show passages.
    """
    width, height = maze.width, maze.height
    maze_colour = get_maze_colour_from_config(config_path, "maze")
    egg_colour = get_maze_colour_from_config(config_path, "egg")
    wall_colour = get_maze_colour_from_config(config_path, "wall")
    path_colour = get_maze_colour_from_config(config_path, "path")
    entry_colour = get_maze_colour_from_config(config_path, "entry")
    exit_colour = get_maze_colour_from_config(config_path, "exit")

    # Get entry/exit coordinates from config
    cfg = parse_config(config_path)
    entry_x = cfg.get('entry_x', 0)
    entry_y = cfg.get('entry_y', 0)
    exit_x = cfg.get('exit_x', width - 1)
    exit_y = cfg.get('exit_y', height - 1)

    # Handle string expressions
    if isinstance(exit_x, str):
        exit_x = eval(
            exit_x, {"width": width, "height": height}
        )
    if isinstance(exit_y, str):
        exit_y = eval(
            exit_y, {"width": width, "height": height}
        )

    vertical, horizontal, render_w, render_h = (
        _build_wall_grids(maze)
    )
    pattern = get_pattern_cells(width, height)

    # Build path walls list
    path_walls_list = []
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        rx1 = x1 * 2 + 1
        ry1 = y1 * 2 + 1
        rx2 = x2 * 2 + 1
        ry2 = y2 * 2 + 1

        if x1 == x2:  # Vertical move
            wall_rx = rx1
            wall_ry = (ry1 + ry2) // 2
        else:  # Horizontal move
            wall_rx = (rx1 + rx2) // 2
            wall_ry = ry1

        path_walls_list.append((wall_rx, wall_ry))

    def render_frame(
            path_cells: Set[Tuple[int, int]],
            path_passages: Set[Tuple[int, int]]
    ) -> None:
        """Render one frame of the animation."""
        # Clear screen and move cursor to top
        os.system('clear')
        sys.stdout.write("\033[2J\033[H")
        # sys.stdout.flush()

        for ry in range(render_h):
            for rx in range(render_w):
                cx = rx // 2
                cy = ry // 2

                curr_in_pat = (cx, cy) in pattern
                left_in_pat = (
                    (cx - 1, cy) in pattern if rx > 0
                    else False
                )
                up_in_pat = (
                    (cx, cy - 1) in pattern if ry > 0
                    else False
                )
                diag_in_pat = (
                    (cx - 1, cy - 1) in pattern
                    if (rx > 0 and ry > 0) else False
                )

                on_path = (cx, cy) in path_cells
                token = ""

                # --- A: Intersections (Corners) ---
                if ry % 2 == 0 and rx % 2 == 0:
                    is_pat_corner = (
                        curr_in_pat or left_in_pat or
                        up_in_pat or diag_in_pat
                    )

                    up = ry > 0 and vertical[ry - 1][rx]
                    down = (
                        ry < render_h - 1 and
                        vertical[ry + 1][rx]
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
                    elif (rx, ry) in path_passages:
                        token = "▓▓▓"
                    else:
                        token = (
                            "═══" if horizontal[ry][rx]
                            else "░░░"
                        )

                # --- C: Vertical segments ---
                elif ry % 2 == 1 and rx % 2 == 0:
                    if curr_in_pat or left_in_pat:
                        token = "║"
                    elif (rx, ry) in path_passages:
                        token = "▓"
                    else:
                        token = (
                            "║" if vertical[ry][rx]
                            else "░"
                        )

                # --- D: Cell Interior ---
                else:
                    if curr_in_pat:
                        token = "███"
                    elif on_path:
                        token = "▓▓▓"
                    else:
                        token = "░░░"

                # Check position
                is_entry = (cx == entry_x and cy == entry_y)
                is_exit = (cx == exit_x and cy == exit_y)
                is_cell_interior = (ry % 2 == 1 and rx % 2 == 1)

                # Colourize
                if token == "███":
                    coloured = colourize_token(
                        token, egg_colour
                    )
                elif is_entry and token == "▓▓▓":
                    coloured = colourize_token(
                        token, entry_colour
                    )
                elif is_exit and is_cell_interior:
                    coloured = colourize_token(
                        token, exit_colour
                    )
                elif token == "▓▓▓" or token == "▓":
                    coloured = colourize_token(
                        token, path_colour
                    )
                elif token == "░░░" or token == "░":
                    coloured = colourize_token(
                        token, maze_colour
                    )
                else:
                    coloured = colourize_token(
                        token, wall_colour
                    )

                sys.stdout.write(coloured)
            sys.stdout.write("\n")
        sys.stdout.flush()

    # Animation: reveal path cells one by one
    time.sleep(0.5)

    for i in range(len(path) + 1):
        path_subset = set(path[:i])
        render_frame(path_subset, set())
        time.sleep(cell_delay)

    # Animation: reveal passages between path cells
    print("\nRevealing passages...\n")
    time.sleep(0.5)

    path_set = set(path)
    for i in range(len(path_walls_list) + 1):
        passages_subset = set(path_walls_list[:i])
        render_frame(path_set, passages_subset)
        time.sleep(wall_delay)

    print("\nMaze solved! (*≧∇≦)ﾉ＜※*・:*:｀♪:*:。*・☆*\n")
