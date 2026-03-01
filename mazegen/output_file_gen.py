"""Output file generation."""
from typing import Tuple, List, Optional
from .maze import Maze
from .solver import find_shortest_path


def path_in_letters(path: Optional[List[Tuple[int, int]]]) -> str:
    """Convert a coordinate path to a string of directions (N, E, S, W)."""
    if not path or len(path) < 2:
        return ""
    moves: dict[tuple[int, int], str] = {
        (0, -1): "N",
        (1, 0): "E",
        (0, 1): "S",
        (-1, 0): "W",
    }
    path_output = []
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i+1]
        step = (x2 - x1, y2 - y1)
        path_output.append(moves.get(step, ""))
    return "".join(path_output)


def maze_in_hex(maze: Maze) -> str:
    """
    Convert the entire maze grid to a hex string representation.
    """
    lines = []
    for y in range(maze.height):
        row = "".join(maze.get_cell(x, y).to_hex()
                      for x in range(maze.width))
        lines.append(row)
    return "\n".join(lines)


def write_output_file(maze: Maze, entry_coord: Tuple[int, int],
                      exit_coord: Tuple[int, int], path: Optional[List[Tuple[int, int]]],
                      filename: str = "maze.txt") -> None:
    """
    Generate the final solution text file.
    """
    entry_x, entry_y = entry_coord
    exit_x, exit_y = exit_coord
    entry_exit = [entry_x, entry_y, exit_x, exit_y]

    for idx, val in enumerate(entry_exit):
        if not isinstance(val, int):
            try:
                entry_exit[idx] = int(val)
            except ValueError:
                entry_exit[idx] = int(eval(str(val), {
                    "width": maze.width,
                    "height": maze.height
                }))
    entry_x, entry_y, exit_x, exit_y = entry_exit

    if path is None:
        path = find_shortest_path(maze, entry_x, entry_y,
                                  exit_x, exit_y)
    with open(filename, "w") as output:
        output.write(maze_in_hex(maze))
        output.write("\n\n")
        output.write(f"{int(entry_x)},{int(entry_y)}\n")
        output.write(f"{int(exit_x)},{int(exit_y)}\n")
        output.write(path_in_letters(path) + "\n")
