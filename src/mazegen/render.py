"""Rendering utilities for mazes."""
from typing import List
from .maze import Maze, Wall


def render_ascii(maze: Maze) -> str:
    """
    Render maze as ASCII art.

    Args:
        maze: Maze to render

    Returns:
        ASCII representation of the maze
    """
    lines: List[str] = []

    # Top border
    lines.append('+' + '---+' * maze.width)

    # Render each row
    for y in range(maze.height):
        # Cell row with vertical walls
        cell_line = '|'
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            # Cell interior
            cell_line += '   '
            # East wall
            if cell.has_wall(Wall.EAST):
                cell_line += '|'
            else:
                cell_line += ' '
        lines.append(cell_line)

        # Bottom walls row
        wall_line = '+'
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            # South wall
            if cell.has_wall(Wall.SOUTH):
                wall_line += '---'
            else:
                wall_line += '   '
            wall_line += '+'
        lines.append(wall_line)

    return '\n'.join(lines)


def render_ascii_compact(maze: Maze) -> str:
    """
    Render maze as compact ASCII art (single character cells).

    Args:
        maze: Maze to render

    Returns:
        Compact ASCII representation of the maze
    """
    lines: List[str] = []

    # Top border
    lines.append('┌' + '─' * (maze.width * 2 - 1) + '┐')

    # Render each row
    for y in range(maze.height):
        line = '│'
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            line += ' '

            # East wall or passage
            if x < maze.width - 1:
                if cell.has_wall(Wall.EAST):
                    line += '│'
                else:
                    line += ' '
        line += '│'
        lines.append(line)

        # South walls row (except for last row)
        if y < maze.height - 1:
            line = '│'
            for x in range(maze.width):
                cell = maze.get_cell(x, y)

                # South wall or passage
                if cell.has_wall(Wall.SOUTH):
                    line += '─'
                else:
                    line += ' '

                # Corner
                if x < maze.width - 1:
                    # Determine corner character based on surrounding walls
                    has_south = cell.has_wall(Wall.SOUTH)
                    has_east = cell.has_wall(Wall.EAST)

                    if has_south and has_east:
                        line += '┼'
                    elif has_south:
                        line += '─'
                    elif has_east:
                        line += '│'
                    else:
                        line += ' '
            line += '│'
            lines.append(line)

    # Bottom border
    lines.append('└' + '─' * (maze.width * 2 - 1) + '┘')

    return '\n'.join(lines)


def render_mlx(maze: Maze) -> str:
    """
    Render maze in MLX format (hex grid).

    MLX format is a simple text representation where each cell
    is represented by its hexadecimal wall encoding.

    Args:
        maze: Maze to render

    Returns:
        MLX representation of the maze
    """
    lines: List[str] = []
    hex_grid = maze.to_hex_grid()

    for row in hex_grid:
        lines.append(' '.join(row))

    return '\n'.join(lines)


def render_mlx_detailed(maze: Maze) -> str:
    """
    Render maze in detailed MLX format with dimensions.

    Args:
        maze: Maze to render

    Returns:
        Detailed MLX representation
    """
    lines: List[str] = []
    lines.append(f"# Maze dimensions: {maze.width}x{maze.height}")
    lines.append("# Wall encoding: N=0x1, E=0x2, S=0x4, W=0x8")
    lines.append("")

    hex_grid = maze.to_hex_grid()
    for y, row in enumerate(hex_grid):
        line = f"{y:3d}: " + ' '.join(f"{cell:>2s}" for cell in row)
        lines.append(line)

    return '\n'.join(lines)
