"""Configuration file parser for maze generation."""
from typing import Dict, Any
import re


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
    if width > 10000 or height > 10000:
        raise ConfigError(
            f"Maze dimensions too large: {width}x{height}. "
            f"Maximum is 10000x10000"
        )

    # Validate algorithm if specified
    if 'algorithm' in config:
        valid_algorithms = ['prim', 'kruskal']
        algo = str(config['algorithm']).lower()
        if algo not in valid_algorithms:
            raise ConfigError(
                f"Invalid algorithm: {config['algorithm']}. "
                f"Must be one of: {', '.join(valid_algorithms)}"
            )
        config['algorithm'] = algo

    # Set defaults
    config.setdefault('algorithm', 'prim')
    config.setdefault('perfect', True)
    config.setdefault('seed', None)
