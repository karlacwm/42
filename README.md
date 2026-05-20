*This project has been created as part of the 42 curriculum by wcheung.*

## Description

This project is about designing a system that finds the most efficient path to send drones from start to end zone, while passing through different types of zone in between them.
The challenge lies in finding the best path, not only considering the shortest path, but as well as traffic, since there are limits with zone capacity and connection capacity.

The map is configured with a txt file which has strict syntactic rules, which will be then passed to the parser and followed by the pathfinder.
The visualisation of the drones is handled with Tkinter, more information can be found in Resources below.

My project structure:

- `Makefile`: defines a set of rules for installing dependencies(flake8 and mypy), running the program, debugging, cleanning up and checking lint
- `main.py`: parse map, run simulation and visualise results
- `parser.py`: parses plain text map files and add zones object into the `Network`
- `network.py`: defines the classes `ZoneType`, `Zone`, `Connection` and `Network`
- `pathfinder.py`: finds least-cost routes with dynamic traffic
- `simulation.py`: turn-based engine that enforces zone and link capacities, restricted-zone rules, and records history (for visualiser)
- `visualiser.py`: a `tkinter` GUI showing zones, links and drone movement, visualising each turn movement

## Instructions

### Usage

Run a map with the Makefile helper or directly with Python:

```bash
make install
make run MAP_FILE=maps/easy/01_linear_path.txt
```
OR

```bash
make install
source drone_venv/bin/activate
python3 main.py maps/easy/01_linear_path.txt
```

### Flake8 and mypy checks

```bash
make lint
make lint-strict
```

### Map format

- `nb_drones: N` — total number of drones
- `hub: NAME X Y [zone=... color=... max_drones=...]` — define a zone
- `start_hub:` / `end_hub:` — special hub zones
- `connection: A-B [max_link_capacity=...]` — link two zones

### Algorithm and Implementation

Pathfinding: a Dijkstra-like algorithm is used for pathfinding.
The `Pathfinder` repeatedly finds the cheapest path while incrementing temporary traffic to reserve link usage.

Connection cost increases as links become used; restricted and priority zones have modified entry costs (in `get_cost`).
This produces behavior similar to Successive Shortest Path approaches for Minimum Cost Maximum Flow problems.

Minimum Cost Maximum Flow problems inspired me to the multi-paths approach in the project,
where drones get their path from the list of path sorted by pathfinder.
Instead of letting all the drones go the same path, I use a `path_list[index % best_cost]` to let the drones get different paths.
The `best_cost` is handled in `main.py` to control the number of best paths to be looped.
This number is not set dynamically for the moment but it is possible.

Simulation controls each turn, and enforcing link capacities, zone capacities, and restricted zone cooldowns.
Drones record their positions each turn for playback.

### Visualisation

The visualiser is implemented with `tkinter`.

The map is drawn on the canvas with a sidebar on the bottom, showing controls options and information about the map file, total drones and turns.
Besides the information in the sidebar, I added a hover effect on zones to display their name, zone type and max capacity.
Zones are drawn as coloured circles and drones as triangular markers.

Controls options:

- Right/Left arrow to step through turns
- Escape to quit

## Resources

Lists of links that I used as reference sorted by topics

- for docstrings
[[1]](https://peps.python.org/pep-0257/)

- for algorithm
[[1]](https://www.codementor.io/blog/basic-pathfinding-explained-with-python-5pil8767c1)
[[2]](https://graphable.ai/blog/pathfinding-algorithms/)
[[3]](https://www.geeksforgeeks.org/dsa/dijkstras-shortest-path-algorithm-greedy-algo-7/)
[[4]](https://www.w3schools.com/dsa/dsa_algo_graphs_dijkstra.php)

- maximum flow
[[1]](https://www.w3schools.com/dsa/dsa_theory_graphs_maxflow.php)

- for visualisation - tkinter
[[1]](https://www.geeksforgeeks.org/python/python-gui-tkinter/)
[[2]](https://steam.oxxostudio.tw/category/python/tkinter/start.html)
[[3]](https://www.tutorialspoint.com/python/tk_pack.htm)
[[4]](https://steam.oxxostudio.tw/category/python/tkinter/canvas.html)
[[5]](https://inventwithpython.com/blog/complete-list-tkinter-colors-valid-and-tested.html)
[[6]](https://www.geeksforgeeks.org/python/python-tkinter-create-different-shapes-using-canvas-class/)
[[7]](https://www.tutorialspoint.com/python/tk_label.htm)
[[8]](https://youtu.be/fGx8-RmaJbg)

- tkinter colours
[[1]](https://inventwithpython.com/blog/complete-list-tkinter-colors-valid-and-tested.html)

- enum
[[1]](https://mimo.org/glossary/python/enum)

- Python module Dataclass
[[1]](https://elshad-karimov.medium.com/unlocking-the-hidden-power-of-dataclasses-field-9fd0f66aa960)
[[2]](https://realpython.com/python-data-classes/)
[[3]](https://www.dataquest.io/blog/how-to-use-python-data-classes/) <!-- Note: Python doesn't accept a non-default attribute after default in both class and functions, so this would throw an error -->
[[4]](https://thenewstack.io/python-dataclasses-a-complete-guide-to-boilerplatefree-objects/)
[[5]](https://www.pythonmorsels.com/customizing-dataclass-fields/) <!-- Note: init=False argument makes a dataclass field that cannot be specified when we make a new instance of the class. default_factory must be a callable with no arguments -->

- property decorator
[[1]](https://www.freecodecamp.org/news/python-property-decorator/)
[[2]](https://www.programiz.com/python-programming/property)
[[31]](https://medium.com/@christopher.kelly1997/python-decorators-and-dynamic-properties-55402a2e1aff)

- readline()
[[1]](https://www.geeksforgeeks.org/python/readline-in-python/)

- enumerate()
[[1]](https://www.geeksforgeeks.org/python/enumerate-in-python/)

- regex
[[1]](https://realpython.com/ref/stdlib/re/)

- queue
[[1]](https://medium.com/@shras_a/queue-in-python-34a74641502e)
[[2]](https://realpython.com/ref/stdlib/queue/)
[[3]](https://www.w3schools.com/python/ref_module_queue.asp)
[[4]](https://www.geeksforgeeks.org/python/heap-queue-or-heapq-in-python/)

- itertools-count()
[[1]](https://stackabuse.com/pythons-itertools-count-cycle-and-chain/)


### AI usage

- helped to verify if my ideas are feasible
- helped with project planning
- explained Python concepts, functions and methods usage, tkinter concepts
- compared algorithms for pathfinding
- helped with debugging and enhance the visualiser
- explained errors I had and provided suggestions to improve my code

<!-- --------------------------------------------
my initial plan
what i need:
- classes for zones and connections and the whole network and drones
- parser and error handling for parser (use pydantic maybe?)
- algorithm for path finding: combine dijkstra and maximum flow
- engine
- visualisation (i'm thinking about tkinter or pygame)
- simulation output
- makefile
- readme
- docstrings

not sure about:
- coordinates as tuples? how do i link them to my classes?
- shortest path is not the most efficient path, look into network flow algorithms (like Edmonds-Karp) or multi-agent pathfinding (MAPF) concepts
- how do i parse the information from txt files of maps and connect them to my classes?
-->

