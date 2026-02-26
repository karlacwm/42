"""Configuration file parser for maze generation."""
from typing import Dict, Any
import re

# from idna import valid_contextj


class ConfigError(Exception):
    """Exception raised for configuration errors."""
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
        if not match:
            raise ConfigError(
                f"Invalid configuration format at line {line_num}: {line}"
            )

        key, value = match.groups()

        # Try to convert value to appropriate type
        value = value.strip()

        # Remove quotes if present
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        # Try to convert to int
        elif value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
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
    # Check required parameters
        if 'width' not in config:
            raise ConfigError("Missing required parameter: width")
        if 'height' not in config:
            raise ConfigError("Missing required parameter: height")

        width = config['width']
        height = config['height']

        # Validate dimensions
        if not isinstance(width, int) or width < 2:
            raise ConfigError(f"Invalid width: {width}. Must be an integer >= 2")
        if not isinstance(height, int) or height < 2:
            raise ConfigError(f"Invalid height: {height}. Must be an integer >= 2")

        # Check for impossibly large mazes
        if width > 100 or height > 100:
            raise ConfigError(
                f"Maze dimensions too large: {width}x{height}. "
                f"Maximum is over 1000x1000"
            )

        # Validate algorithm if specified
        if 'algorithm' in config:
            valid_algorithms = ['prim', 'kruskal', 'iterative_backtracking']
            algo = str(config['algorithm']).lower()
            if algo not in valid_algorithms:
                raise ConfigError(
                    f"Invalid algorithm: {config['algorithm']}. "
                    f"Must be one of: {', '.join(valid_algorithms)}"
                )
            config['algorithm'] = algo

        valid_color = {'white', 'blue_green', 'brown', 'light_gray',
                        'blue', 'marroon', 'forest_green', 'dark_gray',
                        'green', 'lime', 'navy_blue', 'tan',
                        'red', 'pink', 'rust', 'coffee_brown',
                        'black', 'purple', 'dandilion_yellow', 'moon_glow',
                        'orange', 'gray', 'highlighter',
                        'yellow', 'magenta', 'sky_blue'}

        if 'maze_color' in config:
            color = str(config['maze_color']).lower()
            if color not in valid_color:
                raise ConfigError(
                    f"Invalid maze_color: {config['maze_color']}. "
                    f"Must be one of: {', '.join(valid_color)}"
                )
            config['maze_color'] = color

        if 'egg42' in config:
            color = str(config['egg42']).lower()
            if color not in valid_color:
                raise ConfigError(
                    f"Invalid egg42: {config['egg42']}. "
                    f"Must be one of: {', '.join(valid_color)}"
                )
            config['egg42'] = color

        if 'wall_color' in config:
            color = str(config['wall_color']).lower()
            if color not in valid_color:
                raise ConfigError(
                    f"Invalid wall_color: {config['wall_color']}. "
                    f"Must be one of: {', '.join(valid_color)}"
                )
            config['wall_color'] = color
    except ConfigError as e:
        print(e)
        print("Please change invalid value in 'config.txt' before you try again.")

    # # Set defaults
    # config.setdefault('algorithm', 'iterative_backtracking')
    # config.setdefault('perfect', True)
    # config.setdefault('seed', None)
    # config.setdefault('maze_color', 'pink')
    # config.setdefault('egg42', 'yellow')
    # config.setdefault('wall_color', 'white')
