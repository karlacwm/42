"""Rendering utilities for mazes."""
import sys
import time
from typing import List, Tuple, Set
from .maze import Maze, Wall


def get_pattern_cells(width: int, height: int) -> Set[Tuple[int, int]]:
    """Generates (x, y) coordinates for '42' in the center."""

    cx, cy = width // 2, height // 2

    # Offsets for a 3x5 font
    digit_4 = {
        (0, 0), (0, 1), (0, 2),        # Left
        (1, 2),                        # Middle
        (2, 0), (2, 1), (2, 2), (2, 3), (2, 4) # Right
    }
    digit_2 = {
        (0, 0), (1, 0), (2, 0),        # Top
        (2, 1),                        # Right down
        (0, 2), (1, 2), (2, 2),        # Middle
        (0, 3),                        # Left down
        (0, 4), (1, 4), (2, 4)         # Bottom
    }

    start_x = cx - 3
    start_y = cy - 2

    pattern = set()

    for dx, dy in digit_4:
        pattern.add((start_x + dx, start_y + dy))
    for dx, dy in digit_2:
        pattern.add((start_x + 4 + dx, start_y + dy))

    return pattern


def _build_wall_grids(maze: Maze) -> Tuple[List[List[bool]], List[List[bool]], int, int]:
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


def render_unicode(maze: Maze, delay: float = 0.01) -> str:
    width, height = maze.width, maze.height
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
            up_in_pat   = (cx, cy - 1) in pattern if ry > 0 else False
            diag_in_pat = (cx - 1, cy - 1) in pattern if (rx > 0 and ry > 0) else False

            token = ""

            # --- A: Intersections (Corners) ---
            if ry % 2 == 0 and rx % 2 == 0:
                # If any of the 4 surrounding cells is a pattern cell,
                # we recalculate the intersection to ensure a "box" look.
                is_pat_corner = curr_in_pat or left_in_pat or up_in_pat or diag_in_pat

                up = ry > 0 and vertical[ry - 1][rx]
                down = ry < render_h - 1 and vertical[ry + 1][rx]
                left = rx > 0 and horizontal[ry][rx - 1]
                right = rx < render_w - 1 and horizontal[ry][rx + 1]

                # Override: If it's a pattern corner, force the connections
                if is_pat_corner:
                    # Logic: If I'm the Top-Left of a pattern cell, I need Right and Down.
                    # This builds the box connections.
                    u = up or (up_in_pat or diag_in_pat)
                    d = down or (curr_in_pat or left_in_pat)
                    l = left or (left_in_pat or diag_in_pat)
                    r = right or (curr_in_pat or up_in_pat)
                    token = wall_unicode.get((u, r, d, l), "░")
                else:
                    token = wall_unicode.get((up, right, down, left), "░")

            # --- B: Horizontal segments ---
            elif ry % 2 == 0 and rx % 2 == 1:
                # Force wall if cell above or below is a pattern cell
                if curr_in_pat or up_in_pat:
                    token = "═══" # Adjust to 3 wide to fit the ╔═══╗ request
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

            line += token
            sys.stdout.write(token)
            sys.stdout.flush()
            time.sleep(delay)

        lines.append(line)
        sys.stdout.write("\n")

    return "\n".join(lines)


# ╔═══╗
# ║███║
# ╚═══╝

# ╔════╦═══════════════════╦════════════════════════╗
# ║░░░░║░░░░░░░░░░░░░░░░░░░║░░░░░░░░░░░░░░░░░░░░░░░░║
# ║░░░░░░░░░╔═════════╗░░░░░░░░░░════╗░░░░╔═════════╣
# ║░░░░░░░░░║░░░░░░░░░║░░░░░░░░░░░░░░║░░░░║░░░░░░░░░║
# ║░░░░╔════╝░░░░╔════╩══════════════╣░░░░░░░░░░░░░░║
# ║░░░░║░░░░░░░░░║░░░░░░░░░░░░░░░░░░░║░░░░░░░░░║░░░░║
# ║░░░░╚════░░░░░║░░░░╔═════════╗░░░░║░░░░╔════╝░░░░║
# ║░░░░░░░░░░░░░░║░░░░║░░░░░░░░░║░░░░║░░░░║░░░░░░░░░║
# ╠═════════░░░░░║░░░░║░░░░░░░░░░░░░░║░░░░║░░░░░░░░░║
# ║░░░░░░░░░░░░░░║░░░░║░░░░║░░░░░░░░░║░░░░║░░░░║░░░░║
# ╠══════════════╣░░░░╚════╣░░░░░════╩════╣░░░░╚════╣
# ║░░░░░░░░░░░░░░║░░░░░░░░░║░░░░░░░░░░░░░░║░░░░░░░░░║
# ║░░░░░════╗░░░░╚════░░░░░╠═════════░░░░░╚════╗░░░░║
# ║░░░░░░░░░║░░░░░░░░░░░░░░║░░░░░░░░░░░░░░░░░░░║░░░░║
# ║░░░░░░░░░╠══════════════╝░░░░╔═════════╗░░░░║░░░░║
# ║░░░░║░░░░║░░░░░░░░░░░░░░░░░░░║░░░░░░░░░║░░░░║░░░░║
# ║░░░░║░░░░║░░░░░════╦═════════╩════╗░░░░║░░░░║░░░░║
# ║░░░░║░░░░║░░░░░░░░░║░░░░░░░░░░░░░░║░░░░║░░░░║░░░░║
# ║░░░░║░░░░╚═════════╝░░░░░░░░░░════╝░░░░║░░░░░░░░░║
# ║░░░░║░░░░░░░░░░░░░░░░░░░║░░░░░░░░░░░░░░║░░░░░░░░░║
# ╚════╩═══════════════════╩══════════════╩═════════╝
#
# ╔════╦═══════════════════╦════════════════════════╗
# ║░░░░║░░░░░░░░░░░░░░░░░░░║░░░░░░░░░░░░░░░░░░░░░░░░║
# ║░░░░░░░░░╔═════════╗░░░░░░░░░░════╗░░░░╔═════════╣
# ║░░░░░░░░░║░░░░░░░░░║░░░░░░░░░░░░░░║░░░░║░░░░░░░░░║
# ║░░░░╔════╝░░░░╔════╩══════════════╣░░░░░░░░░░░░░░║
# ║░░░░║░░░░░░░░░║░░░░░░░░░░░░░░░░░░░║░░░░░░░░░║░░░░║
# ║░░░░╚════░░░░░║░░░░╔═════════╗░░░░║░░░░╔════╝░░░░║
# ║░░░░░░░░░░░░░░║░░░░║░░░░░░░░░║░░░░║░░░░║░░░░░░░░░║
# ╠═════════░████║░░░░║████░█████████║░░░░║░░░░░░░░░║
# ║░░░░░░░░░░████║░░░░║████║░░░░░████║░░░░║░░░░║░░░░║
# ╠══════════████╣░░░░╚████╣░░░░░████╩════╣░░░░╚════╣
# ║░░░░░░░░░░████║░░░░░████║█████████░░░░░║░░░░░░░░░║
# ║░░░░░════╗██████████████╠████═════░░░░░╚════╗░░░░║
# ║░░░░░░░░░║░░░░░░░░░░████║████░░░░░░░░░░░░░░░║░░░░║
# ║░░░░░░░░░╠══════════████╝█████████═════╗░░░░║░░░░║
# ║░░░░║░░░░║░░░░░░░░░░░░░░░░░░░║░░░░░░░░░║░░░░║░░░░║
# ║░░░░║░░░░║░░░░░════╦═════════╩════╗░░░░║░░░░║░░░░║
# ║░░░░║░░░░║░░░░░░░░░║░░░░░░░░░░░░░░║░░░░║░░░░║░░░░║
# ║░░░░║░░░░╚═════════╝░░░░░░░░░░════╝░░░░║░░░░░░░░░║
# ║░░░░║░░░░░░░░░░░░░░░░░░░║░░░░░░░░░░░░░░║░░░░░░░░░║
# ╚════╩═══════════════════╩══════════════╩═════════╝

# def render_unicode(maze: Maze) -> str:
#     width = maze.width

#     vertical, horizontal, render_w, render_h = _build_wall_grids(maze)

#     if maze.width > 10 and maze.height > 9:
#         pattern = get_pattern_cells(maze.width, maze.height)
#     else:
#         pattern = set()

#     lines = []

#     for ry in range(render_h):
#         line = ""
#         for rx in range(render_w):

#             if ry % 2 == 1 and rx % 2 == 0:
#                 # vertical segment
#                 if vertical[ry][rx]:
#                     if rx == width * 2:
#                         line += "║   "
#                     else:
#                         line += "║░░░"
#                 else:
#                     line += "░░░░"

#             elif ry % 2 == 0 and rx % 2 == 1:
#                 # horizontal segment
#                 if horizontal[ry][rx]:
#                     line += "════"
#                 else:
#                     line += "░░░░"

#             elif ry % 2 == 0 and rx % 2 == 0:
#                 # intersection — compute connections
#                 up = ry > 0 and vertical[ry - 1][rx]╬
#                 down = ry < render_h - 1 and vertical[ry + 1][rx]
#                 left = rx > 0 and horizontal[ry][rx - 1]
#                 right = rx < render_w - 1 and horizontal[ry][rx + 1]

#                 if up and down and left and right:
#                     line += "╬"
#                 elif up and down and left:
#                     line += "╣"
#                 elif up and down and right:
#                     line += "╠"
#                 elif left and right and up:
#                     line += "╩"
#                 elif left and right and down:
#                     line += "╦"
#                 elif up and down:
#                     line += "║"
#                 elif left and right:
#                     line += "═"
#                 elif up and left:
#                     line += "╝"
#                 elif up and right:
#                     line += "╚"
#                 elif down and left:
#                     line += "╗"
#                 elif down and right:
#                     line += "╔"
#                 else:
#                     line += "░"

#             else:
#                 line += "░"

#         lines.append(line)
#     return "\n".join(lines)
# def render_unicode(maze: Maze) -> str:
#     width = maze.width
#     height = maze.height

#     vertical, horizontal, render_w, render_h = _build_wall_grids(maze)

#     # Fetch the 42 pattern
#     if width > 5 and height > 5:
#         pattern = get_pattern_cells(width, height)
#     else:
#         pattern = set()

#     lines = []

#     for ry in range(render_h):
#         line = ""
#         for rx in range(render_w):
#             # 1. Determine if this specific spot is inside a "pattern" cell
#             # Mapping render coordinates back to maze cell coordinates (x, y)
#             cell_x, cell_y = (rx - 1) // 2, (ry - 1) // 2
#             is_pattern = (cell_x, cell_y) in pattern

#             # 2. Vertical Walls/Spaces
#             if ry % 2 == 1 and rx % 2 == 0:
#                 if vertical[ry][rx]:
#                     line += "║" + ("███" if is_pattern else "░░░")
#                 else:
#                     line += "████" if is_pattern else "░░░░"

#             # 3. Horizontal Walls/Spaces
#             elif ry % 2 == 0 and rx % 2 == 1:
#                 line += "████" if is_pattern else ("════" if horizontal[ry][rx] else "░░░░")

#             # 4. Intersections
#             elif ry % 2 == 0 and rx % 2 == 0:
#                 up = ry > 0 and vertical[ry - 1][rx]
#                 down = ry < render_h - 1 and vertical[ry + 1][rx]
#                 left = rx > 0 and horizontal[ry][rx - 1]
#                 right = rx < render_w - 1 and horizontal[ry][rx + 1]

#                 # Use full block if the intersection is part of the pattern path
#                 if is_pattern:
#                     line += "█"
#                 else:
#                     if up and down and left and right: line += "╬"
#                     elif up and down and left: line += "╣"
#                     elif up and down and right: line += "╠"
#                     elif left and right and up: line += "╩"
#                     elif left and right and down: line += "╦"
#                     elif up and down: line += "║"
#                     elif left and right: line += "═"
#                     elif up and left: line += "╝"
#                     elif up and right: line += "╚"
#                     elif down and left: line += "╗"
#                     elif down and right: line += "╔"
#                     else: line += "░"

#             # 5. The Cell Center
#             else:
#                 line += "████" if is_pattern else "░░░░"

#         lines.append(line)
#     return "\n".join(lines)


# def render_unicode_animated(maze: Maze, delay: float = 0.1) -> str:
#     """Render the maze while printing each (x, y) position with a delay."""
#     width = maze.width
#     height = maze.height

#     vertical, horizontal, render_w, render_h = _build_wall_grids(maze)

#     if width > 5 and height > 5:
#         pattern = get_pattern_cells(width, height)
#     else:
#         pattern = set()

#     lines = []
#     for ry in range(render_h):
#         line = ""
#         for rx in range(render_w):
#             cell_x, cell_y = (rx - 1) // 2, (ry - 1) // 2
#             is_pattern = (cell_x, cell_y) in pattern

#             if ry % 2 == 1 and rx % 2 == 0:
#                 # vertical segment
#                 if vertical[ry][rx]:
#                     if is_pattern:
#                         token = "║███"
#                     else:
#                         token = "║   " if rx == width * 2 else "║░░░"
#                 else:
#                     token = "░░░░"

#             elif ry % 2 == 0 and rx % 2 == 1:
#                 # horizontal segment
#                 token = "████" if is_pattern else ("════" if horizontal[ry][rx] else "░░░░")

#             elif ry % 2 == 0 and rx % 2 == 0:
#                 # intersection — compute connections
#                 up = ry > 0 and vertical[ry - 1][rx]
#                 down = ry < render_h - 1 and vertical[ry + 1][rx]
#                 left = rx > 0 and horizontal[ry][rx - 1]
#                 right = rx < render_w - 1 and horizontal[ry][rx + 1]

#                 if up and down and left and right:
#                     token = "╬"
#                 elif up and down and left:
#                     token = "╣"
#                 elif up and down and right:
#                     token = "╠"
#                 elif left and right and up:
#                     token = "╩"
#                 elif left and right and down:
#                     token = "╦"
#                 elif up and down:
#                     token = "║"
#                 elif left and right:
#                     token = "═"
#                 elif up and left:
#                     token = "╝"
#                 elif up and right:
#                     token = "╚"
#                 elif down and left:
#                     token = "╗"
#                 elif down and right:
#                     token = "╔"
#                 else:
#                     token = "░"
#             else:
#                 token = "░"

#             line += token
#             sys.stdout.write(token)
#             sys.stdout.flush()
#             time.sleep(delay)

#         lines.append(line)
#         sys.stdout.write("\n")
#         sys.stdout.flush()

#     return "\n".join(lines)
