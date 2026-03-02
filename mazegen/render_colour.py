"""
Colour rendering utilities for maze visualization.
"""
from typing import Tuple, Dict, Any
from . import colour as colours


# Colour tuple type definition
ColourTuple = Tuple[int, ...] | Any


def get_colour_by_name(colour_name: str) -> ColourTuple:
    """
    Get a colour tuple by name from the colour module.
    Raises AttributeError if colour name doesn't exist
    """
    colour_name_lower = colour_name.lower()
    # the `colours` module is imported above; attribute names are lower‑case
    if hasattr(colours, colour_name_lower):
        return getattr(colours, colour_name_lower)
    raise AttributeError(f"Colour '{colour_name}' not found in colour module")


def colourize_token(token: str, colour: ColourTuple) -> str:
    """
    Apply ANSI colour codes to token.
    Works with any string (walls, cells, or empty space) so the caller
    can uniformly colour an entire maze line or even a whole output
    string.
    """
    r, g, b = colour
    return f"\033[38;2;{r};{g};{b}m{token}\033[0m"


def get_maze_colour_from_config(
        config_path: Dict[str, Any] | str | None,
        what_to_colour: str = ""
) -> ColourTuple:
    """
    Looks up in the config file if there is a valid value for colours,
    if none, sets the colour to default value chosen by luc and weng,
    neon vibe :)
    """
    config: Dict[str, Any]
    if isinstance(config_path, dict):
        config = config_path
    elif isinstance(config_path, str):
        # Backward compatibility path; do not re-validate here to avoid
        # repeated validation side effects during rendering.
        from .config import parse_config
        config = parse_config(config_path)
    else:
        config = {}

    name: str = ""
    if what_to_colour == "maze":
        name = str(config.get("maze_colour"))
    elif what_to_colour == "egg":
        name = str(config.get("egg42"))
    elif what_to_colour == "wall":
        name = str(config.get("wall_colour"))
    elif what_to_colour == "path":
        name = str(config.get("path_colour"))
    elif what_to_colour == "entry":
        name = str(config.get("entry_colour"))
    elif what_to_colour == "exit":
        name = str(config.get("exit_colour"))
    return get_colour_by_name(name)
