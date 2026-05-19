*This project has been created as part of the 42 curriculum by wcheung.*

## Description

This project implements a multi-agent routing simulation that aims to
minimise total travel time by combining shortest-path search with
traffic-aware costs. The core idea is a heuristic Successive Shortest
Path approach: repeatedly run Dijkstra-like searches while increasing
connection costs as links are reserved/used to reflect congestion.

Key components:

- `parser.py`: parses plain-text map files into a `Network` model.
- `network.py`: graph primitives (`Zone`, `Connection`, capacities).
- `pathfinder.py`: computes least-cost routes with dynamic traffic
	penalties (successive shortest-path heuristic).
- `simulation.py`: turn-based engine that enforces zone and link
	capacities, restricted-zone rules, and records history for playback.
- `visualiser.py`: a `tkinter` GUI showing zones, links and drone
	movement history; supports stepping through turns.

Intended input/output:

- Input: map files in `maps/` describing hubs, coordinates, metadata
	and connections.
- Output: console simulation logs plus an optional `tkinter` visual
	playback of the simulation.

Design goals:

- Prefer simple, auditable heuristics over complex optimisations.
- Preserve capacity and restricted-zone semantics required by the
	challenge while allowing dynamic (per-turn) routing decisions.

## Instructions

Installation

Prerequisites:

- Python 3.10 or newer
- `tkinter` (for the GUI visualiser)

Quick setup (recommended):

```bash
python3 -m venv drone_venv
source drone_venv/bin/activate
pip install -r requirements.txt  # optional; otherwise install required packages
```

Running

- Run a single map (CLI + visualiser):

```bash
python3 main.py maps/easy/01_linear_path.txt
```

- Use the `Makefile` helper (example target):

```bash
make run MAP_FILE=maps/easy/01_linear_path.txt
```

- To run headless (no GUI), set `VISUALISER=0` environment variable or
	call the relevant runner that skips the GUI (if available in your
	environment).

Linting and checks

```bash
make lint
pydocstyle .
flake8
```

Notes

- The `maps/` folder contains several example maps ordered by
	difficulty. Start with `maps/easy/` to see expected behaviour.
- If the GUI fails to start, ensure `tkinter` is installed for your
	platform or run the simulation in headless mode.
## Resources

for docstrings
https://peps.python.org/pep-0257/

for algorithm
https://www.codementor.io/blog/basic-pathfinding-explained-with-python-5pil8767c1
https://graphable.ai/blog/pathfinding-algorithms/
https://www.geeksforgeeks.org/dsa/dijkstras-shortest-path-algorithm-greedy-algo-7/
https://www.w3schools.com/dsa/dsa_algo_graphs_dijkstra.php

for visualisation - tkinter
https://www.geeksforgeeks.org/python/python-gui-tkinter/
https://steam.oxxostudio.tw/category/python/tkinter/start.html
https://www.tutorialspoint.com/python/tk_pack.htm
https://steam.oxxostudio.tw/category/python/tkinter/canvas.html
https://inventwithpython.com/blog/complete-list-tkinter-colors-valid-and-tested.html
https://www.geeksforgeeks.org/python/python-tkinter-create-different-shapes-using-canvas-class/
https://www.tutorialspoint.com/python/tk_label.htm
https://youtu.be/fGx8-RmaJbg

maximum flow
https://www.w3schools.com/dsa/dsa_theory_graphs_maxflow.php

enum
https://mimo.org/glossary/python/enum

Python module Dataclass
https://realpython.com/python-data-classes/
https://www.dataquest.io/blog/how-to-use-python-data-classes/
<!-- As a reminder, Python doesn't accept a non-default attribute after default in both class and functions, so this would throw an error -->
https://thenewstack.io/python-dataclasses-a-complete-guide-to-boilerplatefree-objects/
https://www.pythonmorsels.com/customizing-dataclass-fields/
<!-- init=False argument makes a dataclass field that cannot be specified when we make a new instance of the class.
default_factory must be a callable with no arguments -->
https://elshad-karimov.medium.com/unlocking-the-hidden-power-of-dataclasses-field-9fd0f66aa960

property decorator
https://www.freecodecamp.org/news/python-property-decorator/
https://www.programiz.com/python-programming/property
https://medium.com/@christopher.kelly1997/python-decorators-and-dynamic-properties-55402a2e1aff

readline()
https://www.geeksforgeeks.org/python/readline-in-python/

enumerate()
https://www.geeksforgeeks.org/python/enumerate-in-python/

regex
https://realpython.com/ref/stdlib/re/

queue
https://medium.com/@shras_a/queue-in-python-34a74641502e
https://realpython.com/ref/stdlib/queue/
https://www.w3schools.com/python/ref_module_queue.asp
https://www.geeksforgeeks.org/python/heap-queue-or-heapq-in-python/

itertools-count()
https://stackabuse.com/pythons-itertools-count-cycle-and-chain/


AI usage


• A “Description” section that clearly presents the project, including its goal and a brief overview.

• An “Instructions” section containing any relevant information about compilation, installation, and/or execution.

• A “Resources” section listing classic references related to the topic (documentation, articles, tutorials, etc.), as well as a description of how AI was used — specifying for which tasks and which parts of the project.

• A detailed description of your algorithm choices and implementation strategy must also be included.

• Documentation of the visual representation features and how they enhance the user experience.

--------------------------------------------
initial plan
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

also:
- colours:
https://inventwithpython.com/blog/complete-list-tkinter-colors-valid-and-tested.html

------------------------------------------
How to parse and connect to classes:
The standard approach is a line-by-line reader.

Read the file line by line.

When you parse a line starting with hub:, instantiate a new Zone object with the extracted name, coordinates, and metadata. Store this object in a dictionary inside your Network class (e.g., self.zones["roof1"] = Zone(...)).

When you reach a connection: line, extract the two zone names. Look them up in your dictionary, and pass those actual Zone objects into a new Connection object to link them together.

------------------------------------------
the engine
Moving drones simultaneously.

Verifying that a move won't exceed a zone's capacity after outgoing drones have left.

Handling the rule where drones entering a restricted zone must spend exactly 2 turns in transit and cannot wait on the connection.

Formatting and printing the strict step-by-step output required for evaluation (e.g., D1-roof1 D2-corridorA)



maps: $(VENV_PYTHON)
	$(VENV_PYTHON) $(MAIN) maps/easy/01_linear_path.txt
	@echo "Target is less than 6 turns"
	@echo "========================================"
	$(VENV_PYTHON) $(MAIN) maps/easy/02_simple_fork.txt
	@echo "Target is less than 6 turns"
	@echo "========================================"
	$(VENV_PYTHON) $(MAIN) maps/easy/03_basic_capacity.txt
	@echo "Target is less than 8 turns"
	@echo "========================================"

	$(VENV_PYTHON) $(MAIN) maps/medium/01_dead_end_trap.txt
	@echo "Target is less than 15 turns"
	@echo "========================================"
	$(VENV_PYTHON) $(MAIN) maps/medium/02_circular_loop.txt
	@echo "Target is less than 20 turns"
	@echo "========================================"
	$(VENV_PYTHON) $(MAIN) maps/medium/03_priority_puzzle.txt
	@echo "Target is less than 12 turns"
	@echo "========================================"

	$(VENV_PYTHON) $(MAIN) maps/hard/01_maze_nightmare.txt
	@echo "Target is less than 45 turns"
	@echo "========================================"
	$(VENV_PYTHON) $(MAIN) maps/hard/02_capacity_hell.txt
	@echo "Target is less than 60 turns"
	@echo "========================================"
	$(VENV_PYTHON) $(MAIN) maps/hard/03_ultimate_challenge.txt
	@echo "Target is less than 35 turns"
	@echo "========================================"

	$(VENV_PYTHON) $(MAIN) maps/challenger/01_the_impossible_dream.txt
	@echo "Target is less than 45 turns"

### Installation

Prerequisites:

- Python 3.10 or newer
- A virtual environment is recommended

Quick setup:

```bash
python3 -m venv drone_venv
source drone_venv/bin/activate
pip install -r requirements.txt  # if you have one; otherwise install needed packages
```

You can also use the included `drone_venv` for a pre-made virtualenv.

### Usage

Run a map with the Makefile helper or directly with Python:

```bash
# using make (example)
make run MAP_FILE=maps/easy/01_linear_path.txt

# or directly
python3 main.py maps/easy/01_linear_path.txt
```

The program will parse the map file, run the simulation and open the
visualiser (tkinter) showing zones, links and drone movement history.

### Map format (brief)

- `nb_drones: N` — total number of drones
- `hub: NAME X Y [zone=type color=... max_drones=...]` — define a zone
- `start_hub:` / `end_hub:` — special hub zones
- `connection: A-B [max_link_capacity=...]` — link two zones

See the `maps/` directory for several example map files.

### Algorithm and Implementation

- Pathfinding: a Dijkstra-like successive shortest path heuristic is
	used. The `Pathfinder` repeatedly finds the cheapest path while
	incrementing temporary traffic to reserve link usage.
- Connection cost increases as links become used; restricted and
	priority zones have modified entry costs (in `get_cost`). This
	produces behavior similar to Successive Shortest Path approaches for
	Minimum Cost Maximum Flow problems.
- Simulation: the `Simulation` engine moves drones in sorted order
	each turn, enforcing link capacities, zone capacities, and restricted
	zone cooldowns. Drones record their positions each turn for
	playback.

### Visualisation

- Implemented with `tkinter`; zones are drawn as coloured circles and
	drones as triangular markers.
- Controls: Right/Left arrow to step through history, Escape to quit.
- The sidebar shows map details and turn statistics.

### AI usage

- AI was used to add and reformat project docstrings, and to generate
	README content expansions. The code, logic and algorithmic design
	remain hand-authored.

### Development & Linting

Run the project's linters and docstring checks (if configured):

```bash
make lint
# or, for common tools
pydocstyle .
flake8
```
