"""Color rendering utilities for maze visualization."""
from typing import Tuple, Dict, Any
from .maze import Maze, Cell
# import the color module for namespace access
from . import color as colors
import colorsys


# Color tuple type definition
ColorTuple = Tuple[int, ...] | Any


def hsv_to_rgb(h: float, s: float, v: float) -> ColorTuple:
    """
    Convert HSV color to RGB.

    Args:
        h: Hue (0-1)
        s: Saturation (0-1)
        v: Value (0-1)

    Returns:
        RGB color tuple (0-255 each)
    """
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def get_color_by_name(color_name: str) -> ColorTuple:
    """
    Get a color tuple by name from the color module.

    Args:
        color_name: Name of the color (e.g., 'red', 'blue')

    Returns:
        RGB color tuple

    Raises:
        AttributeError: If color name doesn't exist
    """
    color_name_lower = color_name.lower()
    # the `colors` module is imported above; attribute names are lower‑case
    if hasattr(colors, color_name_lower):
        return getattr(colors, color_name_lower)
    raise AttributeError(f"Color '{color_name}' not found in color module")


def blend_colors(color1: ColorTuple, color2: ColorTuple, ratio: float) -> ColorTuple:
    """
    Blend two colors based on a ratio.

    Args:
        color1: First color RGB tuple
        color2: Second color RGB tuple
        ratio: Blend ratio (0.0 = color1, 1.0 = color2)

    Returns:
        Blended RGB color tuple
    """
    ratio = max(0.0, min(1.0, ratio))
    r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
    g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
    b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
    return (r, g, b)


def colorize_token(token: str, color: ColorTuple) -> str:
    """Apply ANSI color codes to token.

    Works with any string (walls, cells, or empty space) so the caller
    can uniformly color an entire maze line or even a whole output
    string.
    """
    r, g, b = color
    return f"\033[38;2;{r};{g};{b}m{token}\033[0m"


def get_maze_color_from_config(config_path: str = "config.txt", what_to_color: str = "") -> ColorTuple:
    """Load configuration file and return the RGB tuple for ``maze_color``.

    The helper wraps :func:`parse_config`/``validate_maze_config`` and
    :func:`get_color_by_name` so callers (like ``render_unicode``) don't
    need to repeat the lookup logic.
    """
    from .config import parse_config, validate_maze_config

    cfg = parse_config(config_path)
    validate_maze_config(cfg)
    name = ""
    if what_to_color == "maze":
        name = cfg.get("maze_color", "white")
    elif what_to_color == "egg":
        name = cfg.get("egg42", "white")
    try:
        return get_color_by_name(name)
    except AttributeError:
        # fall back to white if validation somehow missed it
        return colors.white


class CellColorizer:
    """Apply colors to maze cells based on different criteria."""

    def __init__(self, color_scheme: str = "RED") -> None:
        """
        Initialize the colorizer with a color scheme.

        Args:
            color_scheme: Color scheme name ('RED', 'BLUE', 'GREEN', 'YELLOW',
                         'CYAN', 'PURPLE', 'HSV', or color name from color module)
        """
        self.color_scheme = color_scheme.upper()
        self.distance_data: Dict[Tuple[int, int], float] = {}
        self.max_distance = 1.0
        self.min_distance = 0.0

    def set_distance_data(self, distances: Dict[Tuple[int, int], float]) -> None:
        """
        Set distance data for cells (for gradient coloring).

        Args:
            distances: Dictionary mapping (x, y) to distance values
        """
        self.distance_data = distances
        if distances:
            self.max_distance = max(distances.values()) or 1.0
            self.min_distance = min(distances.values()) or 0.0

    def get_cell_color(self, cell: Cell) -> ColorTuple:
        """
        Get color for a specific cell based on the current scheme.

        Args:
            cell: Cell to colorize

        Returns:
            RGB color tuple
        """
        # HSV scheme - use hue based on distance
        if self.color_scheme == "HSV":
            return self._get_hsv_color(cell)

        # Distance-based gradients
        if self.color_scheme in ["RED", "BLUE", "GREEN", "YELLOW", "CYAN", "PURPLE"]:
            return self._get_gradient_color(cell)

        # Named color from color module
        try:
            return get_color_by_name(self.color_scheme)
        except AttributeError:
            # Fallback to white
            return colors.white

    def _get_hsv_color(self, cell: Cell) -> ColorTuple:
        """
        Get HSV-based color for a cell.

        Args:
            cell: Cell to colorize

        Returns:
            RGB color tuple
        """
        cell_key = (cell.x, cell.y)
        if cell_key in self.distance_data:
            distance = self.distance_data[cell_key]
        else:
            distance = 0

        # Hue based on distance (0-360 degrees)
        hue = (distance / max(self.max_distance, 1)) if self.max_distance > 0 else 0
        return hsv_to_rgb(hue, 1.0, 1.0)

    def _get_gradient_color(self, cell: Cell) -> ColorTuple:
        """
        Get distance-based gradient color for a cell.

        Args:
            cell: Cell to colorize

        Returns:
            RGB color tuple
        """
        cell_key = (cell.x, cell.y)
        distance = self.distance_data.get(cell_key, 0)

        # Calculate intensity based on distance
        if self.max_distance > self.min_distance:
            intensity = (distance - self.min_distance) / (self.max_distance - self.min_distance)
        else:
            intensity = 0

        intensity = max(0, min(1, intensity))
        dark = min(int(255 * intensity), 255)
        bright = min(int(128 + (127 * intensity)), 255)

        # Color mapping
        colors_map = {
            "RED": (bright, dark, dark),
            "BLUE": (dark, dark, bright),
            "GREEN": (dark, bright, dark),
            "YELLOW": (bright, bright, dark),
            "CYAN": (dark, bright, bright),
            "PURPLE": (bright, dark, bright),
        }

        return colors_map.get(self.color_scheme, colors.white)

    def colorize_maze(self, maze: Maze) -> Dict[Tuple[int, int], ColorTuple]:
        """
        Get colors for all cells in a maze.

        Args:
            maze: Maze to colorize

        Returns:
            Dictionary mapping (x, y) coordinates to RGB color tuples
        """
        cell_colors: Dict[Tuple[int, int], ColorTuple] = {}

        for row in maze.cells:
            for cell in row:
                cell_colors[(cell.x, cell.y)] = self.get_cell_color(cell)

        return cell_colors


def get_gradient_color(
    value: float,
    scheme: str = "RED",
    min_val: float = 0.0,
    max_val: float = 1.0
) -> ColorTuple:
    """
    Get a gradient color for a normalized value.

    Args:
        value: Value to map to color
        scheme: Color scheme ('RED', 'BLUE', 'GREEN', 'YELLOW', 'CYAN', 'PURPLE')
        min_val: Minimum value for normalization
        max_val: Maximum value for normalization

    Returns:
        RGB color tuple
    """
    # Normalize value
    if max_val > min_val:
        normalized = (value - min_val) / (max_val - min_val)
    else:
        normalized = 0

    normalized = max(0, min(1, normalized))
    dark = min(int(255 * normalized), 255)
    bright = min(int(128 + (127 * normalized)), 255)

    colors_map = {
        "RED": (bright, dark, dark),
        "BLUE": (dark, dark, bright),
        "GREEN": (dark, bright, dark),
        "YELLOW": (bright, bright, dark),
        "CYAN": (dark, bright, bright),
        "PURPLE": (bright, dark, bright),
    }

    return colors_map.get(scheme.upper(), colors.white)


def create_color_palette(
    num_colors: int,
    start_hue: float = 0.0,
    end_hue: float = 1.0
) -> list[ColorTuple]:
    """
    Create a palette of evenly distributed colors.

    Args:
        num_colors: Number of colors to generate
        start_hue: Starting hue (0-1)
        end_hue: Ending hue (0-1)

    Returns:
        List of RGB color tuples
    """
    palette = []
    for i in range(num_colors):
        if num_colors > 1:
            hue = start_hue + (end_hue - start_hue) * (i / (num_colors - 1))
        else:
            hue = start_hue

        palette.append(hsv_to_rgb(hue, 1.0, 1.0))

    return palette
