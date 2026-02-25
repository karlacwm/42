"""Rendering utilities for mazes."""
from typing import List
from .maze import Maze, Wall


def render_unicode(maze: Maze) -> str:
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

    lines = []

    for ry in range(render_h):
        line = ""
        for rx in range(render_w):

            if ry % 2 == 1 and rx % 2 == 0:
                # vertical segment
                if vertical[ry][rx]:
                    if rx == width * 2:
                        line += "║   "
                    else:
                        line += "║░░░"
                else:
                    line += "░░░░"

            elif ry % 2 == 0 and rx % 2 == 1:
                # horizontal segment
                if horizontal[ry][rx]:
                    line += "════"
                else:
                    line += "░░░░"

            elif ry % 2 == 0 and rx % 2 == 0:
                # intersection — compute connections
                up = ry > 0 and vertical[ry - 1][rx]
                down = ry < render_h - 1 and vertical[ry + 1][rx]
                left = rx > 0 and horizontal[ry][rx - 1]
                right = rx < render_w - 1 and horizontal[ry][rx + 1]

                if up and down and left and right:
                    line += "╬"
                elif up and down and left:
                    line += "╣"
                elif up and down and right:
                    line += "╠"
                elif left and right and up:
                    line += "╩"
                elif left and right and down:
                    line += "╦"
                elif up and down:
                    line += "║"
                elif left and right:
                    line += "═"
                elif up and left:
                    line += "╝"
                elif up and right:
                    line += "╚"
                elif down and left:
                    line += "╗"
                elif down and right:
                    line += "╔"
                else:
                    line += "░"

            else:
                line += "░"

        lines.append(line)
    return "\n".join(lines)
