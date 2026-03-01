"""
A_Maze_Ing - Maze Generation Package.

This package provides maze generation algorithms:
- Prim's,
- Kruskal's, and
- Iterative Backtracking)
with support for perfect mazes, hexadecimal wall encoding, and various
rendering formats with colour support.
"""

from .maze import Maze, Cell, Wall, Direction
from .generator import generate_maze
from .class_maze_generator import MazeGenerator
from .algorithms import PrimGenerator, KruskalGenerator, BacktrackingGenerator
from .render import (render_unicode, render_path_animation, get_pattern_cells)
from .solver import find_shortest_path
from .render_colour import (
    CellColourizer,
    hsv_to_rgb,
    get_colour_by_name,
    blend_colours,
    get_gradient_colour,
    create_colour_palette,
    colourize_token,
    get_maze_colour_from_config
)
from .config import parse_config, validate_maze_config, ConfigError
from .output_file_gen import write_output_file

__version__ = "0.1.0"
__all__ = [
    # Maze structures
    "Maze", "Cell", "Wall",
    "Direction",
    # Generation
    "generate_maze", "MazeGenerator", "PrimGenerator",
    "KruskalGenerator", "BacktrackingGenerator", "get_pattern_cells",
    # Rendering
    "render_unicode", "render_path_animation",
    # Solver
    "find_shortest_path",
    # Colour rendering
    "CellColourizer", "hsv_to_rgb",
    "get_colour_by_name", "blend_colours",
    "get_gradient_colour", "create_colour_palette",
    "colourize_token", "get_maze_colour_from_config",
    # Config
    "parse_config", "validate_maze_config",
    "ConfigError",
    # Output file
    "write_output_file"
]
