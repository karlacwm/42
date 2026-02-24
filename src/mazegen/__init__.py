"""
A_Maze_Ing - Maze Generation Package.

This package provides maze generation algorithms (Prim's and Kruskal's)
with support for perfect mazes, hexadecimal wall encoding, and various
rendering formats.
"""

from .maze import Maze, Cell, Wall, Direction
from .generator import generate_maze, generate_prim, generate_kruskal
from .render import render_ascii, render_ascii_compact, render_mlx, render_mlx_detailed
from .config import parse_config, validate_maze_config, ConfigError

__version__ = "0.1.0"
__all__ = [
    # Maze structures
    "Maze",
    "Cell",
    "Wall",
    "Direction",
    # Generation
    "generate_maze",
    "generate_prim",
    "generate_kruskal",
    # Rendering
    "render_ascii",
    "render_ascii_compact",
    "render_mlx",
    "render_mlx_detailed",
    # Config
    "parse_config",
    "validate_maze_config",
    "ConfigError",
]
