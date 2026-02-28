*This project has been created as part of the 42 curriculum by **``` lde-krui ```** and **``` wcheung ```**.*

# A-Maze-ing  ٩(◕‿◕)۶٩(◕‿◕)۶٩(◕‿◕)۶٩(◕‿◕)۶٩(◕‿◕)۶


## 📌 Description

**A-Maze-ing** is a Python-based algorithmic project about **maze generation** and **maze solving**.

The goal is to build a robust system that generates random and customized mazes, in which the user is able to decide the size and colour of the maze, the algorithm to be used or the maze and if the maze is perfect (there is only one path to solve it) through the file 'config.txt'.

### Complete structure and format of our config file (config.txt):

| Key | Description | Example |
| --- | --- | --- |
| `width` | Maze width in number of cells | `WIDTH=20` |
| `height` | Maze height in number of cells | `HEIGHT=15` |
| `algorithm` | Maze generation algorithm | `algorithm=prim` |
| `perfect` | If 'True', creates exactly one path | `PERFECT=True` |
| `seed` | If none, the generation is random every time | `seed=42` |
| `entry` | Entry coordinates (x,y) | `ENTRY=0,0` |
| `exit` | Exit coordinates (x,y) | `EXIT=19,14` |
| `output_file` | Target filename for generated data | `OUTPUT_FILE=output_maze.txt` |
| `wall_color` | Colour of the maze wall | `wall_color=orange` |
| `maze_color` | Colour of the maze | `maze_color=dandilion_yellow` |
| `egg42` | Colour of the 42 easter egg | `egg42=magenta` |
| `path_color` | Colour of the maze solover path | `path_color=highlighter` |

From each maze generation, there will be a user-interactive menu for the user to choose either to regenerate a new maze, either to show or hide the solution path, or apply different colour settings of the maze. Alongside, an output file is also created for each generation and is overwritten every time after generation, showing the maze in a specific hexadecimal format, the entry and exit coordinates and operation directions of the maze solver.

In our project, we decided on three algorithm on maze generation, which are the Prim's, the Kruskal's, and the iterative backtracking. These three generators generate mazes with different approaches and therefore create mazes with different characteristics. For the maze solver, we used Breadth First Search (BFS) to find the shortest path from the entry to the exit point.

### Maze generation algorithms, and why we chose them
| Algorithm | Reason |
| --- | --- |
| Prim's algorithm | It starts from one cell and slowly grows the maze by adding nearby walls at random. We chose Prim’s because it creates dense, natural-looking mazes with lots of short dead ends, making the maze look interesting and adds challenge to the gameplay. |
| Kruskal's algorithm | This method randomly removes walls while making sure no loops are created. It connects separate sections step by step until everything is linked. We chose Kruskal’s because it shows how the Union-Find data structure works. The mazes it makes feel balanced. |
| Iterative backtracking | This algorithm goes down one path as far as it can, then goes back and tries a new path. We chose it because it’s simple, fast, and easy to code. It creates long hallways with fewer branches. It also looks very different from the mazes made by Prim’s and Kruskal’s, which makes it a good comparison. |

### What part of your code is reusable, and how
| Reusable part | How |
| --- | --- |
| Maze Core Data Structure | The grid and wall system (using N, E, S, W directions) work separately from the generation algorithms. This means we can add new algorithms without changing the maze structure. |
| Generation Interface | All algorithms follow the same format: they take a maze and modify it. Because of this, we can easily plug in new algorithms later. |
| Solver Module (BFS) | The Breadth-First Search solver does not depend on how the maze was created. It can solve any maze that uses our grid format. |
| Configuration Parser | The config.txt reader can be reused in any grid-based project that needs settings from a file. |
| Rendering & Animation Engine | The drawing and color system can also be reused for other projects that show grids or visual simulations. |
| Package Export (mazegen-*) | The project can be packaged and installed. Other Python projects, for example Pac-Man, can then import it and use the maze generator as its own module. |


### Advanced features
Besides the maze generation and solver, we implemented these as addition features:
* multiple maze generation algorithms available as options
* RGB colour
* not only integers, config file takes ` height ` and ` width ` of the maze as input
* maze background colour setting and is changeable in user-interactive menu
* animation for maze generation
* animation for maze solver

---

## 📋 Instructions

**Setting up the virtual environment**

1. `make install` : Installs necessary dependencies (pip).
2. `make lint` or `make lint-strict` : Runs `flake8` and `mypy` to ensure code quality.
3. `make run` : Execute the main program in venv.
4. `make clean` : Cleans up everything.
5. `make re` : Cleans up, reinstalls, and runs the main program.

**Visualizing the maze**

* The visualizer includes an user-interactive menu, which allows the following actions:
* **Re-generate**: Create a new maze instantly.
* **Toggle Path**: Show or hide the shortest solution path.
* **Color Change**: Change the colour of maze wall, maze background or the 42 egg.

**Building the Reusable Module**

* To build the `mazegen-*` package: `python3 -m build`
* This produces a `.whl` or `.tar.gz` file at the root for later installation.

---

## ▶️ Resources

**Resources for maze generation algorithm**:
* [YouTube video about maze generation algorithms](https://m.youtube.com/watch?v=U3meEXvYFsc)
* [prim's algorithm](https://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm)
* [discussion on Stack Overflow](https://stackoverflow.com/questions/29739751/implementing-a-randomly-generated-maze-using-prims-algorithm)
* [wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
* [exploring different algorithms](https://professor-l.github.io/mazes/)

**Unicode**:
* [for drawing shapes and border of the maze](http://xahlee.info/comp/unicode_drawing_shapes.html)

**AI Usage**:
* Used to generate the project description and README structure.
* Assisted in designing the hexagonal wall bitmask logic (Bits 0-3 for N, E, S, W).
* Helped verify the `mypy` strict type-hinting configurations.

* **42 Community**: Special thanks to peers at 42 Heilbronn for logic walkthroughs and peer-reviews.

---

## 👥 Team & Project Management

* **Roles**:

` lde-krui `: maze generation (Kruskal's algorithm and iterative backtracking), maze solver (BFS), render RGB colours, start and end of the maze, maze rendering, maze generation and solver animations, creating imperfect maze.
` wcheung `: maze generation (Prim's algorithm), Makefile and output file automation, implement 42 pattern in the maze, maze colour change, user-interactive menu, readme files.
::::::::(make package exportable)

* **Your anticipated planning and how it evolved until the end**

Our plan was to work intensively and finish everything within one week.

At first, we wanted to implement recursive backtracking for maze generation. But because of Python’s recursion limits (especially with larger mazes), we changed it to an iterative version instead. This avoided recursion depth errors and made the program more stable.

* **What worked well and what could be improved**

The core parts of the project worked very well:
* The maze logic was solid and flexible
* The solver worked correctly and handled different maze types
* The rendering system displayed the maze clearly and smoothly

* **Have you used any specific tools? Which ones?**

` flake8 ` for style checking
` mypy ` (strict mode) for static type checking
` pip ` and ` venv ` for dependency management
` make ` for automation
` build ` for packaging (python3 -m build)
* GitHub for version control
* AI assistance for structuring documentation and validating logic

٩(◕‿◕)۶٩(◕‿◕)۶٩(◕‿◕)۶٩(◕‿◕)۶٩(◕‿◕)۶
