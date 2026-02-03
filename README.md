
*This project has been created as part of the 42 curriculum by **``` lde-krui ```** and **```` wcheung``` **.

# A-Maze-ing

## 📌 Description

**A-Maze-ing** is a Python-based algorithmic project focused on **maze generation**, graph theory, and procedural content creation. The goal is to build a robust system that generates random (and optionally "perfect") mazes, encodes them into a specific hexadecimal format, and provides a visual representation for the user. 

The challenge is to ensure full connectivity between an entry and exit point while adhering to strict structural constraints (no large open areas, coherent wall logic). 

This project is designed to deepen understanding of:

* **Graph Algorithms** (Prim's, Kruskal's, or Recursive Backtracking) 
* **Python 3.10 Best Practices** (Type hinting, `mypy`, `flake8`) 
* **Resource Management** (Context managers and exception handling) 
* **Software Packaging** (Building reusable Python distributions) 



### Configuration keys (config.txt):

| Key | Description | Example |
| --- | --- | --- |
| `WIDTH` | Maze width in number of cells | `WIDTH=20` |
| `HEIGHT` | Maze height in number of cells | `HEIGHT=15` |
| `ENTRY` | Entry coordinates (x,y) | `ENTRY=0,0` |
| `EXIT` | Exit coordinates (x,y) | `EXIT=19,14` |
| `OUTPUT_FILE` | Target filename for generated data | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | If `True`, creates exactly one path | `PERFECT=True` |

---

## Instructions

**Setting up the workspace**

1. `make install` : Installs necessary dependencies (pip/uv). 
2. `make lint` : Runs `flake8` and `mypy` to ensure code quality. 



**Running the Generator**

* Execute the main program: `python3 a_maze_ing.py config.txt` 
* The program will generate the maze data and the shortest path (N, E, S, W) in the specified output file. 



**Visualizing the Maze**

* The visualizer (Terminal ASCII or MLX) allows for several interactions: 
* **Re-generate**: Create a new maze instantly. 
* **Toggle Path**: Show or hide the shortest solution path. 
* **Color Change**: Adjust maze wall colors for better visibility. 
* **The "42"**: Look for the Easter egg pattern in the maze structure! 



**Building the Reusable Module**

* To build the `mazegen-*` package: `python3 -m build` 
* This produces a `.whl` or `.tar.gz` file at the root for later installation. 



---

## ▶️ Resources - What I used to complete the project


**Algorithm**:
* [Insert Algorithm Name, e.g., Prim's Algorithm] was chosen because [Insert Reason, e.g., it creates a more "organic" look compared to backtracker]. 


**AI Usage**:
* Used to generate the project description and README structure. 
* Assisted in designing the hexagonal wall bitmask logic (Bits 0-3 for N, E, S, W). 
* Helped verify the `mypy` strict type-hinting configurations. 
* **42 Curriculum**: Special thanks to peers at 42 Heilbronn for logic walkthroughs and peer-reviews. 
* **Technical Docs**: Python 3.10 `typing` and `contextlib` documentation. 



---

## 🛠️ Reusability & Features

* **The `MazeGenerator` Class**: The core logic is encapsulated in a standalone module that can be imported into any future Python project. 
* **Error Handling**: Graceful management of invalid configurations or impossible parameters to prevent crashes. 
* **Reproducibility**: Supports seed-based generation for consistent results. 


---

## 👥 Team & Project Management

* **Roles**:
* **[lde-krui]**: Logic implementation, `MazeGenerator` packaging, and Makefile automation.
* **[wcheung]**: Logic implementation, `MazeGenerator` packaging, and Makefile automation.


* **[Teammate Name]**: Visual representation (ASCII/MLX), input parsing, and error handling. 
* **Tools**: GitHub (version control), `flake8` (linting), `mypy` (type checking). 
* **Evolution**: Initially planned for [X], but evolved to include [Y] due to [Z].
