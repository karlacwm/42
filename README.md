# A_Maze_Ing

A Python 3.10+ maze generator package featuring Prim's and Kruskal's algorithms for generating perfect mazes, with support for hexadecimal wall encoding and multiple rendering formats.

## Features

- **Perfect Maze Generation**: Generate mazes without loops using Prim's or Kruskal's algorithm
- **Hexadecimal Wall Encoding**: Walls encoded using bits 0-3 (N=0x1, E=0x2, S=0x4, W=0x8)
- **Multiple Rendering Formats**:
  - ASCII art (traditional maze display)
  - Compact ASCII (using box-drawing characters)
  - MLX format (hexadecimal grid)
- **Configuration File Support**: Parse KEY=VALUE configuration files
- **Type Safety**: Full mypy strict type hinting
- **Code Quality**: Passes flake8 standards
- **Error Handling**: Validates maze parameters and rejects impossible configurations

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/Electron968/A_Maze_Ing.git
cd A_Maze_Ing

# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

### As a Package (PEP 517)

```bash
pip install .
```

## Quick Start

### Using Configuration Files

Create a configuration file (e.g., `maze_config.txt`):

```
# Maze configuration
width=10
height=8
algorithm=prim
perfect=true
seed=42
```

Generate a maze:

```python
from mazegen import parse_config, validate_maze_config, generate_maze, render_ascii

# Load configuration
config = parse_config('maze_config.txt')
validate_maze_config(config)

# Generate maze
maze = generate_maze(
    width=config['width'],
    height=config['height'],
    algorithm=config['algorithm'],
    seed=config.get('seed')
)

# Render
print(render_ascii(maze))
```

### Programmatic Usage

```python
from mazegen import generate_maze, render_ascii, render_mlx_detailed

# Generate a 5x5 maze using Prim's algorithm
maze = generate_maze(5, 5, algorithm='prim', seed=42)

# Display as ASCII art
print(render_ascii(maze))

# Display in MLX format (hexadecimal)
print(render_mlx_detailed(maze))
```

## Wall Encoding

Walls are encoded using hexadecimal values with bits 0-3 representing:
- Bit 0 (0x1): North wall
- Bit 1 (0x2): East wall
- Bit 2 (0x4): South wall
- Bit 3 (0x8): West wall

Examples:
- `0xF`: All walls present (1111 in binary)
- `0x0`: No walls (0000 in binary)
- `0x9`: North and West walls (1001 in binary)
- `0x6`: East and South walls (0110 in binary)

## Algorithms

### Prim's Algorithm
A randomized version of Prim's minimum spanning tree algorithm:
1. Start with a random cell
2. Add its walls to a frontier
3. Randomly select a wall from the frontier
4. If it connects to an unvisited cell, remove the wall and add the new cell's walls to the frontier
5. Repeat until all cells are visited

### Kruskal's Algorithm
A randomized version of Kruskal's minimum spanning tree algorithm:
1. Start with all cells isolated
2. Create a list of all possible walls between cells
3. Randomly shuffle the list
4. For each wall, if it connects two separate regions, remove it
5. Continue until all cells are connected

Both algorithms guarantee a "perfect" maze with exactly one path between any two cells.

## Configuration File Format

Configuration files use a simple KEY=VALUE format:

```
# Comments start with #
width=10
height=8
algorithm=prim  # or kruskal
perfect=true
seed=42  # optional, for reproducibility
```

Supported types:
- Integers: `width=10`
- Floats: `value=3.14`
- Booleans: `perfect=true` or `perfect=false`
- Strings: `name="My Maze"` or `name='My Maze'`

## API Reference

### Configuration

```python
from mazegen import parse_config, validate_maze_config, ConfigError

# Parse configuration file
config = parse_config(filepath: str) -> Dict[str, Any]

# Validate maze configuration
validate_maze_config(config: Dict[str, Any]) -> None
```

### Generation

```python
from mazegen import generate_maze, generate_prim, generate_kruskal

# Generate maze with specified algorithm
maze = generate_maze(
    width: int,
    height: int,
    algorithm: str = 'prim',  # 'prim' or 'kruskal'
    seed: Optional[int] = None
) -> Maze

# Generate using specific algorithm
maze = generate_prim(width: int, height: int, seed: Optional[int] = None) -> Maze
maze = generate_kruskal(width: int, height: int, seed: Optional[int] = None) -> Maze
```

### Rendering

```python
from mazegen import render_ascii, render_ascii_compact, render_mlx, render_mlx_detailed

# ASCII art rendering
ascii_maze = render_ascii(maze: Maze) -> str

# Compact ASCII rendering (box-drawing characters)
compact_maze = render_ascii_compact(maze: Maze) -> str

# MLX format (hexadecimal grid)
mlx_maze = render_mlx(maze: Maze) -> str
mlx_detailed = render_mlx_detailed(maze: Maze) -> str
```

### Data Structures

```python
from mazegen import Maze, Cell, Wall, Direction

# Create maze
maze = Maze(width: int, height: int)

# Access cells
cell = maze.get_cell(x: int, y: int) -> Cell

# Wall encoding
Wall.NORTH  # 0x1
Wall.EAST   # 0x2
Wall.SOUTH  # 0x4
Wall.WEST   # 0x8
Wall.ALL    # 0xF
```

## Examples

Run the demo script:

```bash
python examples/demo.py
```

This demonstrates:
- Loading configuration from file
- Generating mazes with both algorithms
- Different rendering formats
- Hexadecimal wall encoding

## Development

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=mazegen --cov-report=html
```

### Code Quality

```bash
# Run flake8
flake8 src/mazegen/ tests/

# Run mypy
mypy src/mazegen/ --strict
```

### Project Structure

```
A_Maze_Ing/
├── src/
│   └── mazegen/
│       ├── __init__.py
│       ├── config.py        # Configuration parser
│       ├── maze.py          # Maze data structures
│       ├── generator.py     # Maze generation algorithms
│       └── render.py        # Rendering functions
├── tests/
│   ├── test_config.py
│   ├── test_maze.py
│   ├── test_generator.py
│   └── test_render.py
├── examples/
│   ├── demo.py
│   └── maze_config.txt
├── pyproject.toml
├── setup.cfg
└── README.md
```

## Requirements

- Python 3.10 or higher
- No external runtime dependencies (stdlib only)
- Development dependencies: flake8, mypy, pytest

## Error Handling

The package includes comprehensive error handling:

- **ConfigError**: Raised for invalid configuration files
- **FileNotFoundError**: Raised when config file doesn't exist
- **ValueError**: Raised for invalid algorithm names

Validation checks:
- Maze dimensions must be at least 2x2
- Maze dimensions must not exceed 10000x10000
- Algorithm must be 'prim' or 'kruskal'

## License

This project is open source. See LICENSE file for details.

## Contributing

Contributions are welcome! Please ensure:
- All tests pass
- Code passes flake8 linting
- Code passes mypy strict type checking
- New features include tests
