*This project has been created as part of the 42 curriculum by wcheung.*

## Description

## Instructions

## Resources

for docstrings
https://peps.python.org/pep-0257/

for algorithm
https://graphable.ai/blog/pathfinding-algorithms/
https://www.geeksforgeeks.org/dsa/dijkstras-shortest-path-algorithm-greedy-algo-7/

for visualisation - tkinter
https://www.geeksforgeeks.org/python/python-gui-tkinter/
https://steam.oxxostudio.tw/category/python/tkinter/start.html

tkinter canvas
https://steam.oxxostudio.tw/category/python/tkinter/canvas.html

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
- algorithm for path finding
- engine
- visualisation (i'm thinking about tkinter or pygame)
- makefile
- readme

not sure about:
- coordinates as tuples? how do i link them to my classes?
- shortest path is not the most efficient path, look into network flow algorithms (like Edmonds-Karp) or multi-agent pathfinding (MAPF) concepts
- how do i parse the information from txt files of maps and connect them to my classes?

also:

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
