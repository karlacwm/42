"""
A_Maze_Ing - Maze Generation Package.

This package provides maze generation algorithms (Prim's, Kruskal's, and Recursive Backtracking)
with support for perfect mazes, hexadecimal wall encoding, and various
rendering formats with color support.
"""

from .maze import Maze, Cell, Wall, Direction
from .generator import generate_maze, generate_prim, generate_kruskal
from .recursive_backtracking import generate_recursive_backtracking
from .render import render_ascii, render_ascii_compact, render_mlx, render_mlx_detailed
from .render_color import (
    CellColorizer,
    hsv_to_rgb,
    get_color_by_name,
    blend_colors,
    get_gradient_color,
    create_color_palette,
)
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
    "generate_recursive_backtracking",
    # Rendering
    "render_ascii",
    "render_ascii_compact",
    "render_mlx",
    "render_mlx_detailed",
    # Color rendering
    "CellColorizer",
    "hsv_to_rgb",
    "get_color_by_name",
    "blend_colors",
    "get_gradient_color",
    "create_color_palette",
    # Config
    "parse_config",
    "validate_maze_config",
    "ConfigError",
]
