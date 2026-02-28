"""Configuration file parser for maze generation."""
from typing import Dict, Any
import re


class ConfigError(Exception):
    """Exception raised for configuration errors."""
    pass


class DimensionError(Exception):
    """Exception raised for dimension errors."""
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
        if 'seed' not in config:
            raise ConfigError("Missing required parameter: seed")
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
    except (DimensionError, KeyError) as e:
        print(e)
        height = config['height'] = 10
        width = config['width'] = 20

    # Calculate the "42" pattern cells (same logic as Maze.is_valid)
    cx, cy = width // 2, height // 2
    digit_4 = {
        (0, 0), (0, 1), (0, 2),
        (1, 2),
        (2, 2), (2, 3), (2, 4)
    }
    digit_2 = {
        (0, 0), (1, 0), (2, 0),
        (2, 1),
        (0, 2), (1, 2), (2, 2),
        (0, 3),
        (0, 4), (1, 4), (2, 4)
    }
    start_x = cx - 3
    start_y = cy - 2
    pattern_42 = set()
    for dx, dy in digit_4:
        pattern_42.add((start_x + dx, start_y + dy))
    for dx, dy in digit_2:
        pattern_42.add((start_x + 4 + dx, start_y + dy))

    # Validate algorithm if specified
    try:
        if 'algorithm' in config:
            valid_algorithms = ['prim', 'kruskal', 'iterative_backtracking']
            algo = str(config['algorithm']).lower()
            if algo == '':
                raise ConfigError("Algorithm cannot be empty,"
                                  " using default 'iterative_backtracking'")
            if algo not in valid_algorithms:
                raise ConfigError(
                    f"Invalid algorithm: {config['algorithm']}. "
                    f"Must be one of: {', '.join(valid_algorithms)}"
                )
            config['algorithm'] = algo
    except ConfigError as e:
        print(e)

    try:
        if 'perfect' in config:
            if not isinstance(config['perfect'], bool):
                raise ConfigError(
                    f"Invalid perfect value: {config['perfect']}."
                    f"Must be a boolean (true/false)"
                )
            if config['perfect'] == '':
                raise ConfigError("perfect cannot be empty,"
                                  " using default True")
    except ConfigError as e:
        print(e)

    try:
        if 'seed' in config:
            if not isinstance(config['seed'], int):
                raise ConfigError(
                    f"Invalid seed value: {config['seed']}. "
                    f"Must be an integer"
                )
            if config['seed'] == '':
                raise ConfigError("seed cannot be empty, using default None")
    except ConfigError as e:
        print(e)

    try:
        if 'entry_x' in config:
            entry_x = config['entry_x']
            if entry_x == '':
                raise ConfigError("entry_x cannot be empty, using default 0")

            # Evaluate expression if it's a string
            if isinstance(entry_x, str):
                try:
                    entry_x = eval(entry_x, {"width": width, "height": height})
                except Exception:
                    raise ConfigError(
                        f"Invalid entry_x expression: {config['entry_x']}")
            config['entry_x'] = entry_x
        if 'entry_y' in config:
            entry_y = config['entry_y']
            if entry_y == '':
                raise ConfigError("entry_y cannot be empty, using default 0")

            # Evaluate expression if it's a string
            if isinstance(entry_y, str):
                try:
                    entry_y = eval(entry_y, {"width": width, "height": height})
                except Exception:
                    raise ConfigError(
                        f"Invalid entry_y expression: {config['entry_y']}")
            config['entry_y'] = entry_y
            if not isinstance(entry_x, int) or not isinstance(entry_y, int):
                raise ConfigError(
                    f"Invalid integer coordinates: ({entry_x}, {entry_y})")

            # Basic bounds check
            if not (0 <= entry_x < width and 0 <= entry_y < height):
                raise ConfigError(
                    f"Invalid entry point: ({entry_x}, {entry_y}). "
                    f"Must be within maze bounds (0-{width-1}, 0-{height-1})")

            # Check if entry falls on the "42" pattern
            if (entry_x, entry_y) in pattern_42:
                raise ConfigError(
                    f"Invalid entry point: ({entry_x}, {entry_y}). "
                    f"Cannot place entry on the '42' pattern in the "
                    f"center of the maze")
    except ConfigError as e:
        print(e)

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
                raise ConfigError("entry_color cannot be empty,"
                                  " using default 'green'")
            if color not in valid_entry:
                raise ConfigError(
                    f"Invalid entry_color: {config['entry_color']}. "
                    f"Must be one of: {', '.join(valid_entry)}"
                )
            config['entry_color'] = color
    except ConfigError as e:
        print(e)

    try:
        if 'exit_x' in config:
            exit_x = config['exit_x']
            if exit_x == '':
                raise ConfigError(
                    "exit_x cannot be empty, using default width - 1")
            # Evaluate expression if it's a string
            if isinstance(exit_x, str):
                try:
                    exit_x = eval(exit_x, {"width": width, "height": height})
                except Exception:
                    raise ConfigError(
                        f"Invalid exit_x expression: {config['exit_x']}")
            config['exit_x'] = exit_x
        if 'exit_y' in config:
            exit_y = config['exit_y']
            if exit_y == '':
                raise ConfigError(
                    "exit_y cannot be empty, using default height - 1")

            # Evaluate expression if it's a string
            if isinstance(exit_y, str):
                try:
                    exit_y = eval(exit_y, {"width": width, "height": height})
                except Exception:
                    raise ConfigError(
                        f"Invalid exit_y expression: {config['exit_y']}")
            config['exit_y'] = exit_y
            if not isinstance(exit_x, int) or not isinstance(exit_y, int):
                raise ConfigError(
                    f"Invalid exit coordinates: ({exit_x}, {exit_y})")

            # Basic bounds check
            if not (0 <= exit_x < width and 0 <= exit_y < height):
                raise ConfigError(
                    f"Invalid exit point: ({exit_x}, {exit_y}). "
                    f"Must be within maze bounds (0-{width-1}, 0-{height-1})")

            # Check if exit falls on the "42" pattern
            if (exit_x, exit_y) in pattern_42:
                raise ConfigError(
                    f"Invalid exit point: ({exit_x}, {exit_y}). "
                    f"Cannot place exit on the '42' pattern in the "
                    f"center of the maze")
            if exit_x == entry_x and exit_y == entry_y:
                raise ConfigError(
                    f"Exit point ({exit_x}, {exit_y}) cannot be the same "
                    f"as entry point ({entry_x}, {entry_y})")
    except ConfigError as e:
        print(e)

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
                raise ConfigError("exit_color cannot be empty,"
                                  " using default 'red'")
            if color not in valid_exit:
                raise ConfigError(
                    f"Invalid exit_color: {config['exit_color']}. "
                    f"Must be one of: {', '.join(valid_exit)}"
                )
            config['exit_color'] = color
    except ConfigError as e:
        print(e)

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
                raise ConfigError("wall_color cannot be empty,"
                                  " using default 'black'")
            if color not in valid_colors:
                raise ConfigError(
                    f"Invalid wall_color: {config['wall_color']}. "
                    f"Must be one of: {', '.join(valid_colors)}"
                )
            config['wall_color'] = color
    except ConfigError as e:
        print(e)

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
                raise ConfigError("maze_color cannot be empty,"
                                  " using default 'yellow'")
            if color not in valid_color:
                raise ConfigError(
                    f"Invalid maze_color: {config['maze_color']}. "
                    f"Must be one of: {', '.join(valid_color)}"
                )
            config['maze_color'] = color
    except ConfigError as e:
        print(e)

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
                raise ConfigError("egg42 cannot be empty,"
                                  " using default 'pink'")
            if color not in valid_42:
                raise ConfigError(
                    f"Invalid egg42: {config['egg42']}. "
                    f"Must be one of: {', '.join(valid_42)}"
                )
            config['egg42'] = color
    except ConfigError as e:
        print(e)

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
                raise ConfigError("path_color cannot be empty,"
                                  " using default 'blue'")
            if color not in valid_path:
                raise ConfigError(
                    f"Invalid path_color: "
                    f"{config['path_color']}. "
                    f"Must be one of: "
                    f"{', '.join(valid_path)}"
                )
            config['path_color'] = color
    except ConfigError as e:
        print(e)
        config['path_color'] = 'blue'

    # Set defaults
    config.setdefault('width', 20)
    config.setdefault('algorithm', 'iterative_backtracking')
    config.setdefault('entry_x', 0)
    config.setdefault('entry_y', 0)
    config.setdefault('exit_x', width - 1)
    config.setdefault('exit_y', height - 1)
    config.setdefault('perfect', True)
    config.setdefault('seed', None)
    config.setdefault('maze_color', 'yellow')
    config.setdefault('egg42', 'pink')
    config.setdefault('wall_color', 'orange')
    config.setdefault('entry_color', 'green')
    config.setdefault('exit_color', 'red')
