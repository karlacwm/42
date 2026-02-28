"""Configuration file parser for maze generation."""
from typing import Dict, Any
import re
from .pattern42 import get_pattern_cells


class ConfigError(Exception):
    """Exception raised for configuration errors."""
    pass


class DimensionError(ConfigError):
    """Exception raised for dimension errors."""
    pass


class AlgorithmError(ConfigError):
    """Exception raised for invalid algorithm errors."""
    pass


class PerfectError(ConfigError):
    """Exception raised for invalid perfect parameter errors."""
    pass


class SeedError(ConfigError):
    """Exception raised for invalid seed parameter errors."""
    pass


class EntryExitError(ConfigError):
    """Exception raised for invalid entry/exit point errors."""
    pass


class ColorError(ConfigError):
    """Exception raised for invalid color errors for walls, maze, entry, exit, or "42" pattern."""
    pass


class FortyTwoError(ConfigError):
    """Exception raised for invalid "42" pattern errors."""
    pass


def parse_config(filepath: str) -> Dict[str, Any]:
    """
    Parse a KEY=VALUE configuration file.

    Args:
        filepath: Path to the configuration file

    Returns:
        Dictionary with parsed configuration values

    Raises:
        ConfigError: If configuration file is invalid
        FileNotFoundError: If configuration file doesn't exist
    """
    config: Dict[str, Any] = {}

    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {filepath}")

    for line_num, line in enumerate(lines, 1):
        # Strip whitespace and skip empty lines and comments
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        # Parse KEY=VALUE format
        match = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)$', line)
        try:
            if not match:
                raise ConfigError(
                    f"Invalid configuration format at line {line_num}: {line}"
                )
        except ConfigError as e:
            print(f"Error in config file '{filepath}': {e}")
            continue

        key, value = match.groups()

        # Try to convert value to appropriate type
        value = value.strip()

        # Remove quotes if present
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        # Try to convert to int
        elif value.isdigit() or (value.startswith('-')
                                 and value[1:].isdigit()):
            value = int(value)
        # Try to convert to float
        elif '.' in value:
            try:
                value = float(value)
            except ValueError:
                pass  # Keep as string
        # Convert boolean values
        elif value.lower() in ('true', 'false'):
            value = value.lower() == 'true'
        config[key] = value
    return config


def validate_maze_config(config: Dict[str, Any]) -> None:
    """
    Validate maze configuration parameters.

    Args:
        config: Configuration dictionary

    Raises:
        ConfigError: If configuration is invalid
    """
    try:
        # if 'width' not in config:
        #     raise ConfigError("Missing required parameter: width")
        # if 'height' not in config:
        #     raise ConfigError("Missing required parameter: height")
        if 'algorithm' not in config:
            raise ConfigError("Missing required parameter: algorithm")
        if 'perfect' not in config:
            raise ConfigError("Missing required parameter: perfect")
        if 'entry_x' not in config:
            raise ConfigError("Missing required parameter: entry_x")
        if 'entry_y' not in config:
            raise ConfigError("Missing required parameter: entry_y")
        if 'exit_x' not in config:
            raise ConfigError("Missing required parameter: exit_x")
        if 'exit_y' not in config:
            raise ConfigError("Missing required parameter: exit_y")
        if 'wall_color' not in config:
            raise ConfigError("Missing required parameter: wall_color")
        if 'maze_color' not in config:
            raise ConfigError("Missing required parameter: maze_color")
        if 'egg42' not in config:
            raise ConfigError("Missing required parameter: egg42")
    except ConfigError as e:
        print(e)

    # Validate dimensions

    try:
        width = config['width']
        height = config['height']
        if width == '' or height == '':
            raise DimensionError("Width and height cannot be empty,"
                                 " using defaults (width=20, height=10)")
        if not isinstance(width, int) or width < 7:
            raise DimensionError(
                f"Invalid width: {width}. Must be an integer >= 7")
        if not isinstance(height, int) or height < 7:
            raise DimensionError(
                f"Invalid height: {height}. Must be an integer >= 7")
        if width > 100 or height > 100:
            raise DimensionError(
                f"Maze dimensions too large: {width}x{height}. "
                f"Maximum is over 100x100"
            )
        pattern_42 = get_pattern_cells(width, height)
    except (DimensionError, KeyError) as e:
        print(e)

    # Calculate the "42" pattern cells (same logic as Maze.is_valid)

    # Validate algorithm if specified
    try:
        if 'algorithm' in config:
            valid_algorithms = ['prim', 'kruskal', 'iterative_backtracking']
            algo = str(config['algorithm']).lower()
            if algo == '':
                raise AlgorithmError("Algorithm cannot be empty,"
                                     " using default 'iterative_backtracking'")
            if algo not in valid_algorithms:
                raise AlgorithmError(
                    f"Invalid algorithm: {config['algorithm']}. "
                    f"Must be one of: {', '.join(valid_algorithms)}"
                )
            config['algorithm'] = algo
    except AlgorithmError as e:
        print(e)
        config['algorithm'] = 'iterative_backtracking'

    try:
        if 'perfect' in config:
            if not isinstance(config['perfect'], bool):
                raise PerfectError(
                    f"Invalid perfect value: {config['perfect']}."
                    f"Must be a boolean (true/false)"
                )
            if config['perfect'] == '':
                raise PerfectError("perfect cannot be empty,"
                                   " using default True")
    except PerfectError as e:
        print(e)
        config['perfect'] = True

    try:
        if 'seed' in config:
            if not isinstance(config['seed'], int):
                raise SeedError(
                    f"Invalid seed value: {config['seed']}. "
                    f"Must be an integer"
                )
            if config['seed'] == '':
                raise SeedError("seed cannot be empty, using default None"
                                "or just comment it out")
    except SeedError as e:
        print(e)
        config['seed'] = None

    # Validate entry and exit points
    try:
        if 'entry_x' in config:
            entry_x = config['entry_x']
            if entry_x == '':
                raise EntryExitError("entry_x cannot be empty, using default 0")

            # Evaluate expression if it's a string
            if isinstance(entry_x, str):
                try:
                    entry_x = eval(entry_x, {"width": width, "height": height})
                except Exception:
                    raise EntryExitError(
                        f"Invalid entry_x expression: {config['entry_x']}")
            config['entry_x'] = entry_x
        if 'entry_y' in config:
            entry_y = config['entry_y']
            if entry_y == '':
                raise EntryExitError("entry_y cannot be empty, using default 0")

            # Evaluate expression if it's a string
            if isinstance(entry_y, str):
                try:
                    entry_y = eval(entry_y, {"width": width, "height": height})
                except Exception:
                    raise EntryExitError(
                        f"Invalid entry_y expression: {config['entry_y']}")
            config['entry_y'] = entry_y
            if not isinstance(entry_x, int) or not isinstance(entry_y, int):
                raise EntryExitError(
                    f"Invalid integer coordinates: ({entry_x}, {entry_y})")

            # Basic bounds check
            if not (0 <= entry_x < width and 0 <= entry_y < height):
                raise EntryExitError(
                    f"Invalid entry point: ({entry_x}, {entry_y}). "
                    f"Must be within maze bounds (0-{width-1}, 0-{height-1})")

            # Check if entry falls on the "42" pattern
            if (entry_x, entry_y) in pattern_42:
                raise EntryExitError(
                    f"Invalid entry point: ({entry_x}, {entry_y}). "
                    f"Cannot place entry on the '42' pattern in the "
                    f"center of the maze")
        config['entry_x'] = entry_x
        config['entry_y'] = entry_y
    except EntryExitError as e:
        print(e)
        entry_x = config['entry_x'] = 0
        entry_y = config['entry_y'] = 0

    try:
        if 'entry_color' in config:
            valid_entry = ['white', 'blue_green', 'brown', 'light_gray',
                           'blue', 'marroon', 'forest_green', 'dark_gray',
                           'lime', 'navy_blue', 'tan', 'green', 'red',
                           'pink', 'rust', 'coffee_brown',
                           'black', 'purple', 'dandilion_yellow',
                           'moon_glow', 'orange', 'gray', 'highlighter',
                           'yellow', 'magenta', 'sky_blue']
            color = str(config['entry_color']).lower()
            if color == '':
                raise ColorError("entry_color cannot be empty,"
                                 " using default 'green'")
            if color not in valid_entry:
                raise ColorError(
                    f"Invalid entry_color: {config['entry_color']}. "
                    f"Must be one of: {', '.join(valid_entry)}"
                )
            config['entry_color'] = color
    except ColorError as e:
        print(e)
        config['entry_color'] = 'green'

    try:
        if 'exit_x' in config:
            exit_x = config['exit_x']
            if exit_x == '':
                raise EntryExitError(
                    "exit_x cannot be empty, using default width - 1")
            # Evaluate expression if it's a string
            if isinstance(exit_x, str):
                try:
                    exit_x = eval(exit_x, {"width": width, "height": height})
                except Exception:
                    raise EntryExitError(
                        f"Invalid exit_x expression: {config['exit_x']}")
            config['exit_x'] = exit_x
        if 'exit_y' in config:
            exit_y = config['exit_y']
            if exit_y == '':
                raise EntryExitError(
                    "exit_y cannot be empty, using default height - 1")

            # Evaluate expression if it's a string
            if isinstance(exit_y, str):
                try:
                    exit_y = eval(exit_y, {"width": width, "height": height})
                except Exception:
                    raise EntryExitError(
                        f"Invalid exit_y expression: {config['exit_y']}")
            config['exit_y'] = exit_y
            if not isinstance(exit_x, int) or not isinstance(exit_y, int):
                raise EntryExitError(
                    f"Invalid exit coordinates: ({exit_x}, {exit_y})")

            # Basic bounds check
            if not (0 <= exit_x < width and 0 <= exit_y < height):
                raise EntryExitError(
                    f"Invalid exit point: ({exit_x}, {exit_y}). "
                    f"Must be within maze bounds (0-{width-1}, 0-{height-1})")

            # Check if exit falls on the "42" pattern
            if (exit_x, exit_y) in pattern_42:
                raise EntryExitError(
                    f"Invalid exit point: ({exit_x}, {exit_y}). "
                    f"Cannot place exit on the '42' pattern in the "
                    f"center of the maze")
            if exit_x == entry_x and exit_y == entry_y:
                raise EntryExitError(
                    f"Exit point ({exit_x}, {exit_y}) cannot be the same "
                    f"as entry point ({entry_x}, {entry_y})")
    except EntryExitError as e:
        print(e)
        exit_x = config['exit_x'] = width - 1
        exit_y = config['exit_y'] = height - 1

    try:
        if 'exit_color' in config:
            valid_exit = ['white', 'blue_green', 'brown', 'light_gray',
                          'blue', 'marroon', 'forest_green', 'dark_gray',
                          'lime', 'navy_blue', 'tan', 'green', 'red',
                          'pink', 'rust', 'coffee_brown',
                          'black', 'purple', 'dandilion_yellow',
                          'moon_glow', 'orange', 'gray', 'highlighter',
                          'yellow', 'magenta', 'sky_blue']
            color = str(config['exit_color']).lower()
            if color == '':
                raise ColorError("exit_color cannot be empty,"
                                 " using default 'red'")
            if color not in valid_exit:
                raise ColorError(
                    f"Invalid exit_color: {config['exit_color']}. "
                    f"Must be one of: {', '.join(valid_exit)}"
                )
            config['exit_color'] = color
    except ColorError as e:
        print(e)
        config['exit_color'] = 'red'

    try:
        if 'wall_color' in config:
            valid_colors = ['white', 'blue_green', 'brown', 'light_gray',
                            'blue', 'marroon', 'forest_green', 'dark_gray',
                            'lime', 'navy_blue', 'tan', 'green', 'red',
                            'pink', 'rust', 'coffee_brown',
                            'black', 'purple', 'dandilion_yellow', 'moon_glow',
                            'orange', 'gray', 'highlighter',
                            'yellow', 'magenta', 'sky_blue']
            color = str(config['wall_color']).lower()
            if color == '':
                raise ColorError("wall_color cannot be empty,"
                                 " using default 'black'")
            if color not in valid_colors:
                raise ColorError(
                    f"Invalid wall_color: {config['wall_color']}. "
                    f"Must be one of: {', '.join(valid_colors)}"
                )
            config['wall_color'] = color
    except ColorError as e:
        print(e)
        config['wall_color'] = 'orange'

    try:
        if 'maze_color' in config:
            valid_color = ['white', 'blue_green', 'brown', 'light_gray',
                           'blue', 'marroon', 'forest_green', 'dark_gray',
                           'lime', 'navy_blue', 'tan', 'green', 'red',
                           'pink', 'rust', 'coffee_brown',
                           'black', 'purple', 'dandilion_yellow', 'moon_glow',
                           'orange', 'gray', 'highlighter',
                           'yellow', 'magenta', 'sky_blue']
            color = str(config['maze_color']).lower()
            if color == '':
                raise ColorError("maze_color cannot be empty,"
                                 " using default 'yellow'")
            if color not in valid_color:
                raise ColorError(
                    f"Invalid maze_color: {config['maze_color']}. "
                    f"Must be one of: {', '.join(valid_color)}"
                )
            config['maze_color'] = color
    except ColorError as e:
        print(e)
        config['maze_color'] = 'yellow'

    try:
        if 'egg42' in config:
            valid_42 = ['white', 'blue_green', 'brown', 'light_gray',
                        'blue', 'marroon', 'forest_green', 'dark_gray',
                        'green', 'lime', 'navy_blue', 'tan',
                        'red', 'pink', 'rust', 'coffee_brown',
                        'black', 'purple', 'dandilion_yellow',
                        'moon_glow', 'orange', 'gray', 'highlighter',
                        'yellow', 'magenta', 'sky_blue']
            color = str(config['egg42']).lower()
            if color == '':
                raise ColorError("egg42 cannot be empty,"
                                 " using default 'pink'")
            if color not in valid_42:
                raise ColorError(
                    f"Invalid egg42: {config['egg42']}. "
                    f"Must be one of: {', '.join(valid_42)}"
                )
            config['egg42'] = color
    except ColorError as e:
        print(e)
        config['egg42'] = 'pink'

    try:
        if 'path_color' in config:
            valid_path = ['white', 'blue_green', 'brown',
                          'light_gray', 'blue', 'marroon',
                          'forest_green', 'dark_gray',
                          'lime', 'navy_blue', 'tan', 'green', 'red',
                          'pink', 'rust', 'coffee_brown', 'black',
                          'purple', 'dandilion_yellow', 'moon_glow',
                          'orange', 'gray', 'highlighter', 'yellow',
                          'magenta', 'sky_blue']
            color = str(config['path_color']).lower()
            if color == '':
                raise ColorError("path_color cannot be empty,"
                                 " using default 'blue'")
            if color not in valid_path:
                raise ColorError(
                    f"Invalid path_color: "
                    f"{config['path_color']}. "
                    f"Must be one of: "
                    f"{', '.join(valid_path)}"
                )
            config['path_color'] = color
    except ColorError as e:
        print(e)
        config['path_color'] = 'highlighter'
