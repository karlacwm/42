"""Colour rendering utilities for maze visualization."""
from typing import Tuple, Dict, Any
from .maze import Maze, Cell
from . import colour as colours
import colorsys


# Colour tuple type definition
ColourTuple = Tuple[int, ...] | Any


def hsv_to_rgb(h: float, s: float, v: float) -> ColourTuple:
    """
    Convert HSV colour to RGB.

    Args:
        h: Hue (0-1)
        s: Saturation (0-1)
        v: Value (0-1)

    Returns:
        RGB colour tuple (0-255 each)
    """
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def get_colour_by_name(colour_name: str) -> ColourTuple:
    """
    Get a colour tuple by name from the colour module.

    Args:
        colour_name: Name of the colour (e.g., 'red', 'blue')

    Returns:
        RGB colour tuple

    Raises:
        AttributeError: If colour name doesn't exist
    """
    colour_name_lower = colour_name.lower()
    # the `colours` module is imported above; attribute names are lower‑case
    if hasattr(colours, colour_name_lower):
        return getattr(colours, colour_name_lower)
    raise AttributeError(f"Colour '{colour_name}' not found in colour module")


def blend_colours(
        colour1: ColourTuple, colour2: ColourTuple, ratio: float
) -> ColourTuple:
    """
    Blend two colours based on a ratio.

    Args:
        colour1: First colour RGB tuple
        colour2: Second colour RGB tuple
        ratio: Blend ratio (0.0 = colour1, 1.0 = colour2)

    Returns:
        Blended RGB colour tuple
    """
    ratio = max(0.0, min(1.0, ratio))
    r = int(colour1[0] * (1 - ratio) + colour2[0] * ratio)
    g = int(colour1[1] * (1 - ratio) + colour2[1] * ratio)
    b = int(colour1[2] * (1 - ratio) + colour2[2] * ratio)
    return (r, g, b)


def colourize_token(token: str, colour: ColourTuple) -> str:
    """Apply ANSI colour codes to token.

    Works with any string (walls, cells, or empty space) so the caller
    can uniformly colour an entire maze line or even a whole output
    string.
    """
    r, g, b = colour
    return f"\033[38;2;{r};{g};{b}m{token}\033[0m"


def get_maze_colour_from_config(
        config_path: str = "config.txt",
        what_to_colour: str = ""
) -> ColourTuple:
    """Load configuration file and return the RGB tuple for ``maze_colour``.

    The helper wraps :func:`parse_config`/``validate_maze_config`` and
    :func:`get_colour_by_name` so callers (like ``render_unicode``) don't
    need to repeat the lookup logic.
    """
    from .config import parse_config, validate_maze_config

    cfg = parse_config(config_path)
    config = validate_maze_config(cfg)
    name = ""
    if what_to_colour == "maze":
        name = config.get("maze_colour")
    elif what_to_colour == "egg":
        name = config.get("egg42")
    elif what_to_colour == "wall":
        name = config.get("wall_colour")
    elif what_to_colour == "path":
        name = config.get("path_colour")
    elif what_to_colour == "entry":
        name = config.get("entry_colour")
    elif what_to_colour == "exit":
        name = config.get("exit_colour")
    try:
        return get_colour_by_name(name)
    except AttributeError:
        # fall back to white if validation somehow missed it
        return colours.white


class CellColourizer:
    """Apply colours to maze cells based on different criteria."""

    def __init__(self, colour_scheme: str = "RED") -> None:
        """
        Initialize the colourizer with a colour scheme.

        Args:
            colour_scheme: Colour scheme name ('RED', 'BLUE', 'GREEN',
                         'YELLOW', 'CYAN', 'PURPLE', 'HSV', or colour name
                         from colour module)
        """
        self.colour_scheme = colour_scheme.upper()
        self.distance_data: Dict[Tuple[int, int], float] = {}
        self.max_distance = 1.0
        self.min_distance = 0.0

    def set_distance_data(
            self, distances: Dict[Tuple[int, int], float]
    ) -> None:
        """
        Set distance data for cells (for gradient colouring).

        Args:
            distances: Dictionary mapping (x, y) to distance values
        """
        self.distance_data = distances
        if distances:
            self.max_distance = max(distances.values()) or 1.0
            self.min_distance = min(distances.values()) or 0.0

    def get_cell_colour(self, cell: Cell) -> ColourTuple:
        """
        Get colour for a specific cell based on the current scheme.

        Args:
            cell: Cell to colourize

        Returns:
            RGB colour tuple
        """
        # HSV scheme - use hue based on distance
        if self.colour_scheme == "HSV":
            return self._get_hsv_colour(cell)

        # Distance-based gradients
        if self.colour_scheme in [
            "RED", "BLUE", "GREEN", "YELLOW", "CYAN", "PURPLE"
        ]:
            return self._get_gradient_colour(cell)

        # Named colour from colour module
        try:
            return get_colour_by_name(self.colour_scheme)
        except AttributeError:
            # Fallback to white
            return colours.white

    def _get_hsv_colour(self, cell: Cell) -> ColourTuple:
        """
        Get HSV-based colour for a cell.

        Args:
            cell: Cell to colourize

        Returns:
            RGB colour tuple
        """
        cell_key = (cell.x, cell.y)
        if cell_key in self.distance_data:
            distance = self.distance_data[cell_key]
        else:
            distance = 0

        # Hue based on distance (0-360 degrees)
        hue = (
            (distance / max(self.max_distance, 1))
            if self.max_distance > 0 else 0
        )
        return hsv_to_rgb(hue, 1.0, 1.0)

    def _get_gradient_colour(self, cell: Cell) -> ColourTuple:
        """
        Get distance-based gradient colour for a cell.

        Args:
            cell: Cell to colourize

        Returns:
            RGB colour tuple
        """
        cell_key = (cell.x, cell.y)
        distance = self.distance_data.get(cell_key, 0)

        # Calculate intensity based on distance
        if self.max_distance > self.min_distance:
            intensity = (
                (distance - self.min_distance) /
                (self.max_distance - self.min_distance)
            )
        else:
            intensity = 0

        intensity = max(0, min(1, intensity))
        dark = min(int(255 * intensity), 255)
        bright = min(int(128 + (127 * intensity)), 255)

        # Colour mapping
        colours_map = {
            "RED": (bright, dark, dark),
            "BLUE": (dark, dark, bright),
            "GREEN": (dark, bright, dark),
            "YELLOW": (bright, bright, dark),
            "CYAN": (dark, bright, bright),
            "PURPLE": (bright, dark, bright),
        }

        return colours_map.get(self.colour_scheme, colours.white)

    def colourize_maze(self, maze: Maze) -> Dict[Tuple[int, int], ColourTuple]:
        """
        Get colours for all cells in a maze.

        Args:
            maze: Maze to colourize

        Returns:
            Dictionary mapping (x, y) coordinates to RGB colour tuples
        """
        cell_colours: Dict[Tuple[int, int], ColourTuple] = {}

        for row in maze.cells:
            for cell in row:
                cell_colours[(cell.x, cell.y)] = self.get_cell_colour(cell)

        return cell_colours


def get_gradient_colour(
    value: float,
    scheme: str = "RED",
    min_val: float = 0.0,
    max_val: float = 1.0
) -> ColourTuple:
    """
    Get a gradient colour for a normalized value.

    Args:
        value: Value to map to colour
        scheme: Colour scheme ('RED', 'BLUE', 'GREEN', 'YELLOW',
                'CYAN', 'PURPLE')
        min_val: Minimum value for normalization
        max_val: Maximum value for normalization

    Returns:
        RGB colour tuple
    """
    # Normalize value
    if max_val > min_val:
        normalized = (value - min_val) / (max_val - min_val)
    else:
        normalized = 0

    normalized = max(0, min(1, normalized))
    dark = min(int(255 * normalized), 255)
    bright = min(int(128 + (127 * normalized)), 255)

    colours_map = {
        "RED": (bright, dark, dark),
        "BLUE": (dark, dark, bright),
        "GREEN": (dark, bright, dark),
        "YELLOW": (bright, bright, dark),
        "CYAN": (dark, bright, bright),
        "PURPLE": (bright, dark, bright),
    }

    return colours_map.get(scheme.upper(), colours.white)


def create_colour_palette(
    num_colours: int,
    start_hue: float = 0.0,
    end_hue: float = 1.0
) -> list[ColourTuple]:
    """
    Create a palette of evenly distributed colours.

    Args:
        num_colours: Number of colours to generate
        start_hue: Starting hue (0-1)
        end_hue: Ending hue (0-1)

    Returns:
        List of RGB colour tuples
    """
    palette = []
    for i in range(num_colours):
        if num_colours > 1:
            hue = start_hue + (end_hue - start_hue) * (i / (num_colours - 1))
        else:
            hue = start_hue

        palette.append(hsv_to_rgb(hue, 1.0, 1.0))

    return palette
