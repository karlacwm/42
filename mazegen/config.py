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


class ColourError(ConfigError):
    """Exception raised for invalid colour errors for walls, maze, entry, exit, or "42" pattern."""
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


valid_colour = {
    'white', 'blue_green', 'brown', 'light_gray',
    'blue', 'marroon', 'forest_green', 'dark_gray',
    'lime', 'navy_blue', 'tan', 'green', 'red',
    'pink', 'rust', 'coffee_brown',
    'black', 'purple', 'dandelion_yellow', 'moon_glow',
    'orange', 'gray', 'highlighter',
    'yellow', 'magenta', 'sky_blue'}


def validate_maze_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate maze configuration parameters.

    Args:
        config: Configuration dictionary

    Raises:
        ConfigError: If configuration is invalid
    """
    try:
        if 'width' not in config:
            raise DimensionError("Missing required parameter: width")
        if 'height' not in config:
            raise DimensionError("Missing required parameter: height")
        if 'algorithm' not in config:
            raise AlgorithmError("Missing required parameter: algorithm")
        if 'perfect' not in config:
            raise PerfectError("Missing required parameter: perfect")
        if 'entry' not in config:
            raise EntryExitError("Missing required parameter: entry")
        if 'exit' not in config:
            raise EntryExitError("Missing required parameter: exit")
        if 'wall_colour' not in config:
            raise ColourError("Missing required parameter: wall_colour")
        if 'maze_colour' not in config:
            raise ColourError("Missing required parameter: maze_colour")
        if 'egg42' not in config:
            raise ColourError("Missing required parameter: egg42")
    except ConfigError as e:
        print(f"{e}"
              "\n. ݁₊ ⊹ . ݁ ⟡ ݁ . ⊹ ₊ ݁."
              "Default values for maze generation applied."
              ". ݁₊ ⊹ . ݁ ⟡ ݁ . ⊹ ₊ ݁.")
        pass

    # Validate dimensions
    try:
        if 'width' in config and 'height' in config:
            width = config['width']
            height = config['height']
            if width == '' or height == '':
                raise DimensionError("Width and height cannot be empty,"
                                     " using defaults (width=16, height=16)")
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
        else:
            width = config['width'] = 16
            height = config['height'] = 16
    except (DimensionError, KeyError) as e:
        print(f"{e}"
              "\n. ݁₊ ⊹ . ݁ ⟡ ݁ . ⊹ ₊ ݁."
              "Default values for maze generation applied."
              ". ݁₊ ⊹ . ݁ ⟡ ݁ . ⊹ ₊ ݁.")
        width = config['width'] = 16
        height = config['height'] = 16

    pattern_42 = get_pattern_cells(width, height)

    def _parse_tuple_key(key: str) -> tuple[int, int]:
        val = str(config.get(key, "")).strip()
        parts = [p.strip() for p in val.split(',')]
        if len(parts) != 2:
            raise EntryExitError(f"Invalid {key} tuple: {val}")
        try:
            x = parts[0]
            y = parts[1]
            if isinstance(x, str):
                x = eval(x, {"width": width, "height": height})
            if isinstance(y, str):
                y = eval(y, {"width": width, "height": height})
            return int(x), int(y)
        except Exception:
            raise EntryExitError(f"Invalid {key} expression: {val}")

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
        else:
            config['algorithm'] = 'iterative_backtracking'
    except AlgorithmError as e:
        print(f"{e}"
              "\n. ݁₊ ⊹ . ݁ ⟡ ݁ . ⊹ ₊ ݁."
              "Default values for maze generation applied."
              ". ݁₊ ⊹ . ݁ ⟡ ݁ . ⊹ ₊ ݁.")
        config['algorithm'] = 'iterative_backtracking'

    # Validate perfect parameter if specified
    try:
        if 'perfect' in config:
            if not isinstance(config['perfect'], bool):
                raise PerfectError(
                    f"Invalid perfect value: {config['perfect']}."
                    f"Must be a boolean (true/false)"
                )
        else:
            config['perfect'] = True
    except PerfectError as e:
        print(f"{e}"
              "\n. ݁₊ ⊹ . ݁ ⟡ ݁ . ⊹ ₊ ݁."
              "Default values for maze generation applied."
              ". ݁₊ ⊹ . ݁ ⟡ ݁ . ⊹ ₊ ݁.")
        config['perfect'] = True

    try:
        if 'seed' in config:
            if not isinstance(config['seed'], int):
                raise SeedError(
                    f"Invalid seed value: {config['seed']}. "
                    f"Must be an integer"
                )
        else:
            config['seed'] = None
    except SeedError as e:
        print(f"{e}"
              "\n. ݁₊ ⊹ . ݁ ⟡ ݁ . ⊹ ₊ ݁."
              "Default values for maze generation applied."
              ". ݁₊ ⊹ . ݁ ⟡ ݁ . ⊹ ₊ ݁.")
        config['seed'] = None

    # Validate entry and exit points
    try:
        if 'entry' in config:
            entry_x, entry_y = _parse_tuple_key('entry')
            config['entry_x'], config['entry_y'] = entry_x, entry_y
            if entry_x is None:
                raise EntryExitError("entry_x cannot be empty, using default 0")

            # Evaluate expression if it's a string
            if isinstance(entry_x, str):
                try:
                    entry_x = eval(entry_x, {"width": width, "height": height})
                except Exception:
                    raise EntryExitError(
                        f"Invalid entry_x expression: {config['entry']}")
            config['entry_x'] = entry_x
            if entry_y is None:
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
        else:
            entry_x = config['entry_x'] = 0
            entry_y = config['entry_y'] = 0
    except EntryExitError as e:
        print(f"{e}"
              "\n. ݁₊ ⊹ . ݁ ⟡ ݁ . ⊹ ₊ ݁."
              "Default values for maze generation applied."
              ". ݁₊ ⊹ . ݁ ⟡ ݁ . ⊹ ₊ ݁.")
        entry_x = config['entry_x'] = 0
        entry_y = config['entry_y'] = 0

    try:
        if 'entry_colour' in config:
            colour = str(config['entry_colour']).lower()
            if colour == '':
                raise ColourError("entry_colour cannot be empty,"
                                  " using default 'green'")
            if colour not in valid_colour:
                raise ColourError(
                    f"Invalid entry_colour: {config['entry_colour']}. "
                    f"Must be one of: {', '.join(valid_colour)}"
                )
            config['entry_colour'] = colour
        else:
            config['entry_colour'] = 'green'
    except ColourError as e:
        print(f"{e}"
              "\n. ݁₊ ⊹ . ݁ ⟡ ݁ . ⊹ ₊ ݁."
              "Default values for maze generation applied."
              ". ݁₊ ⊹ . ݁ ⟡ ݁ . ⊹ ₊ ݁.")
        config['entry_colour'] = 'green'

    try:
        if 'exit' in config:
            exit_x, exit_y = _parse_tuple_key('exit')
            config['exit_x'], config['exit_y'] = exit_x, exit_y
            if exit_x is None:
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
            if exit_y is None:
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
        else:
            exit_x = config['exit_x'] = width - 1
            exit_y = config['exit_y'] = height - 1
    except EntryExitError as e:
        print(f"{e}"
              "\n. ݁₊ ⊹ . ݁ ⟡ ݁ . ⊹ ₊ ݁."
              "Default values for maze generation applied."
              ". ݁₊ ⊹ . ݁ ⟡ ݁ . ⊹ ₊ ݁.")
        exit_x = config['exit_x'] = width - 1
        exit_y = config['exit_y'] = height - 1

    try:
        if 'exit_colour' in config:
            colour = str(config['exit_colour']).lower()
            if colour == '':
                raise ColourError("exit_colour cannot be empty,"
                                  " using default 'red'")
            if colour not in valid_colour:
                raise ColourError(
                    f"Invalid exit_colour: {config['exit_colour']}. "
                    f"Must be one of: {', '.join(valid_colour)}"
                )
            config['exit_colour'] = colour
        else:
            config['exit_colour'] = 'red'
    except ColourError as e:
        print(f"{e}"
              "\n. ݁₊ ⊹ . ݁ ⟡ ݁ . ⊹ ₊ ݁."
              "Default values for maze generation applied."
              ". ݁₊ ⊹ . ݁ ⟡ ݁ . ⊹ ₊ ݁.")
        config['exit_colour'] = 'red'

    try:
        if 'wall_colour' in config:
            colour = str(config['wall_colour']).lower()
            if colour == '':
                raise ColourError("wall_colour cannot be empty,"
                                  " using default 'yellow'")
            if colour not in valid_colour:
                raise ColourError(
                    f"Invalid wall_colour: {config['wall_colour']}. "
                    f"Must be one of: {', '.join(valid_colour)}"
                )
            config['wall_colour'] = colour
        else:
            config['wall_colour'] = 'yellow'
    except ColourError as e:
        print(f"{e}"
              "\n. ݁₊ ⊹ . ݁ ⟡ ݁ . ⊹ ₊ ݁."
              "Default values for maze generation applied."
              ". ݁₊ ⊹ . ݁ ⟡ ݁ . ⊹ ₊ ݁.")

    try:
        if 'maze_colour' in config:
            colour = str(config['maze_colour']).lower()
            if colour == '':
                raise ColourError("maze_colour cannot be empty,"
                                  " using default 'black'")
            if colour not in valid_colour:
                raise ColourError(
                    f"Invalid maze_colour: {config['maze_colour']}. "
                    f"Must be one of: {', '.join(valid_colour)}"
                )
            config['maze_colour'] = colour
        else:
            config['maze_colour'] = 'black'
    except ColourError as e:
        print(f"{e}"
              "\n. ݁₊ ⊹ . ݁ ⟡ ݁ . ⊹ ₊ ݁."
              "Default values for maze generation applied."
              ". ݁₊ ⊹ . ݁ ⟡ ݁ . ⊹ ₊ ݁.")
        config['maze_colour'] = 'black'

    try:
        if 'egg42' in config:
            colour = str(config['egg42']).lower()
            if colour == '':
                raise ColourError("egg42 cannot be empty,"
                                  " using default 'magenta'")
            if colour not in valid_colour:
                raise ColourError(
                    f"Invalid egg42: {config['egg42']}. "
                    f"Must be one of: {', '.join(valid_colour)}"
                )
            config['egg42'] = colour
        else:
            config['egg42'] = 'magenta'
    except ColourError as e:
        print(f"{e}"
              "\n. ݁₊ ⊹ . ݁ ⟡ ݁ . ⊹ ₊ ݁."
              "Default values for maze generation applied."
              ". ݁₊ ⊹ . ݁ ⟡ ݁ . ⊹ ₊ ݁.")
        config['egg42'] = 'magenta'

    try:
        if 'path_colour' in config:
            colour = str(config['path_colour']).lower()
            if colour == '':
                raise ColourError("path_colour cannot be empty,"
                                  " using default 'highlighter'")
            if colour not in valid_colour:
                raise ColourError(
                    f"Invalid path_colour: "
                    f"{config['path_colour']}. "
                    f"Must be one of: "
                    f"{', '.join(valid_colour)}"
                )
            config['path_colour'] = colour
        else:
            config['path_colour'] = 'highlighter'
    except ColourError as e:
        print(f"{e}"
              "\n. ݁₊ ⊹ . ݁ ⟡ ݁ . ⊹ ₊ ݁."
              "Default values for maze generation applied."
              ". ݁₊ ⊹ . ݁ ⟡ ݁ . ⊹ ₊ ݁.")
        config['path_colour'] = 'highlighter'

    return config
