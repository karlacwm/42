*This project has been created as part of the 42 curriculum by **```lde-krui```** and **```wcheung```**.*

# Documentation for the `mazegen` Module

**mazegen** is a Python package that generates, solves, and renders mazes.

It is designed to be **reused** in other projects (like games, data visualizations, or pathfinding simulations).

## 📦 Installation

To use this module in your own project, install it via `pip` from the root directory:

```bash
pip install .
```

## 🛠️ Instantiate and use

The primary entry point is the `generate_maze` factory function. Here is a quick way to get a maze running:

```python
from mazegen import generate_maze, render_unicode

# 1. Create a 20x10 Maze
my_maze = generate_maze(width=20, height=10, algorithm="prim")

# 2. Print it to the console
print(render_unicode(my_maze))
```

## 📘 How to use the module

The main way to create a maze is the `generate_maze()` function.
Use the factory function `generate_maze()` to create a new maze instance.
It returns a `Maze` object containing the grid and walls.


## ⚙️ Available parameters
The `generate_maze` function accepts the following arguments to customize your maze:
| Parameter | Type | Required? | Description|
| --- | ---| --- | --- |
| `width` | int | yes | Number of columns |
| `height` | int | yes | Number of rows |
| `algorithm` | str | no | Algorithm to use. Options: "prim", "kruskal", "iterative_backtracking". |
| `seed` | int | no | Random seed for reproducibility. If None, totally random |
| `perfect` | bool | no | "If True, generates a perfect maze (single path). If False, allows loops |
| `loops` | int | no | "If `perfect=False`, specifies how many internal walls to remove to create loops |

## 🧱 Access the generated structure: the Maze Object

When you generate a maze, you get a `Maze` object. Here is how to use it in your game or application.

Attributes:

* `maze.width`: Integer width of the grid.
* `maze.height`: Integer height of the grid.
* `maze.cells`: A 2D list (list of lists) containing Cell objects.

Each Cell uses a Bitmask (IntFlag) to store wall data. This allows for efficient memory usage and fast bitwise operations.
| Wall | Binary | Bit value |
| --- | --- | --- |
| Wall.NORTH | 0001  | 1
| Wall.EAST | 0010 | 2 |
| Wall.SOUTH | 0100 | 4 |
| Wall.WEST | 1000 | 8 |
| Wall.ALL | 1111 | 15 |

```Python
# Get the cell at column 5, row 3
cell = my_maze.get_cell(x=5, y=3)

# Check coordinates
print(f"Cell is at {cell.x}, {cell.y}")

# Access the raw 2D grid list (Type: List[List[Cell]])
all_cells = maze.cells

# Check walls (Returns True if wall exists)
from mazegen import Wall
if cell.has_wall(Wall.NORTH):
    print("You cannot go North!")
```

## 🛠️ Access the generated structure: the MazeGenerator Class

If you want to add your own algorithm (e.g., Wilson's Algorithm), you should inherit from the `MazeGenerator` base class, just like how multiple algorithms are handled in `mazegen/algorithms.py`.
This ensures your new algorithm is compatible with the rest of the project.

Class: `MazeGenerator`

This is an "Abstract Base Class" (blueprint). You must not use it directly; instead, create a child class that uses it.

1. Required Attributes
When initializing, the class automatically stores:
* `self.width` (int): Grid width.
* `self.height` (int): Grid height.
* `self.seed` (int or None): Random seed.

2. Methods to Implement
You must implement the `generate()` method in a child class.
```
    generate(self) -> Maze
```
* Parameter: None (uses self.width and self.height).
* Return: a Maze object.


```Python
# Generate a 20x15 maze using Kruskal's algorithm
maze = generate_maze(
    width=20,
    height=15,
    algorithm="kruskal",
    seed=42
)
```

3. Helper Methods
The class provides built-in tools:
```
    get_protected_cells(self) -> Set[Tuple[int, int]]
```
* Returns the coordinates of the "42" pattern in the center.
* Usage: Check this set during generation so you don't carve walls inside the pattern.


## 💡 Usage example
```Python
import random
from mazegen import MazeGenerator, Maze

class ExampleGenerator(MazeGenerator):
    """
    A simple generator that randomly removes East or South walls.
    """
    def generate(self) -> Maze:
        # Initialize an empty grid with all walls
        maze = Maze(self.width, self.height)

        # Get the protected "42" pattern coordinates
        protected = self.get_protected_cells()

        return maze

# Usage
custom_gen = ExampleGenerator(width=20, height=10, seed=123)
my_maze = custom_gen.generate()

# Rendering
from mazegen import render_unicode
print(render_unicode(my_maze))
```
