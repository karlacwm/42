"""Maze data structures and wall encoding."""
from typing import List, Tuple, Set
from enum import IntFlag


class Wall(IntFlag):
    """
    Wall encoding using bits 0-3 for N, E, S, W directions.
    """
    NORTH = 0x1
    EAST = 0x2
    SOUTH = 0x4
    WEST = 0x8
    ALL = 0xF


class Direction:
    """Direction constants (dx, dy) for maze navigation."""
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)
    ALL = [NORTH, EAST, SOUTH, WEST]

    @staticmethod
    def to_wall(direction: Tuple[int, int]) -> Wall:
        """Convert direction to wall flag."""
        if direction == Direction.NORTH:
            return Wall.NORTH
        elif direction == Direction.EAST:
            return Wall.EAST
        elif direction == Direction.SOUTH:
            return Wall.SOUTH
        elif direction == Direction.WEST:
            return Wall.WEST
        raise ValueError(f"Invalid direction: {direction}")

    @staticmethod
    def opposite(direction: Tuple[int, int]) -> Tuple[int, int]:
        """Get opposite direction."""
        dx, dy = direction
        return (-dx, -dy)


class Cell:
    """Represents a single cell in the maze."""

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes a cell, starts with all walls.
        """
        self.x = x
        self.y = y
        self.walls = Wall.ALL

    def remove_wall(self, wall: Wall) -> None:
        """Remove a wall from this cell."""
        self.walls &= ~wall

    def has_wall(self, wall: Wall) -> bool:
        """Check if cell has a specific wall."""
        return bool(self.walls & wall)

    def to_hex(self) -> str:
        """Convert cell walls to hexadecimal format."""
        return f"{self.walls:X}"

    def __repr__(self) -> str:
        """String representation of cell."""
        return f"Cell({self.x}, {self.y}, walls={self.to_hex()})"


class Maze:
    """Represents a maze grid."""

    def __init__(self, width: int, height: int) -> None:
        """
        Initialize a maze.
        """
        self.width = width
        self.height = height
        self.cells: List[List[Cell]] = []

        for y in range(height):
            row: List[Cell] = []
            for x in range(width):
                row.append(Cell(x, y))
            self.cells.append(row)

    def get_cell(self, x: int, y: int) -> Cell:
        """Get cell at coordinates."""
        return self.cells[y][x]

    def is_valid(self, x: int, y: int) -> bool:
        """Check if coordinates are valid."""
        return 0 <= x < self.width and 0 <= y < self.height

    def get_neighbors(
            self, x: int, y: int
    ) -> List[Tuple[int, int, Tuple[int, int]]]:
        """
        Gets list of tuples (nx, ny, direction) for each valid neighbor
        """
        neighbors = []
        for direction in Direction.ALL:
            dx, dy = direction
            nx, ny = x + dx, y + dy
            if self.is_valid(nx, ny):
                neighbors.append((nx, ny, direction))
        return neighbors

    def remove_wall_between(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """
        Remove the shared wall between two adjacent cells,
        remove_wall() called on both cells but opposite direction.
        """
        dx = x2 - x1
        dy = y2 - y1
        direction = (dx, dy)

        self.cells[y1][x1].remove_wall(Direction.to_wall(direction))
        self.cells[y2][x2].remove_wall(Direction.to_wall((-dx, -dy)))

    def to_hex_grid(self) -> List[List[str]]:
        """
        Convert maze to hexadecimal grid representation.
        """
        return [[cell.to_hex() for cell in row] for row in self.cells]

    def add_loops(
            self,
            forbidden: Set[Tuple[int, int]],
            loops: int
    ) -> None:
        """
        Creates imperfect maze by removing internal walls, but
        never removes walls of 42 pattern or outer borders and
        prevents creation of 2x2 blocks of completely open cells.
        [forbidden]: Set of coordinates that must not be removed
        [loops]: Maximum number of walls to remove
        """
        import random

        valid_candidates = []

        # Collect all internal walls that are safe to remove
        for y in range(self.height):
            for x in range(self.width):
                cell = self.get_cell(x, y)

                # Check south wall
                if y < self.height - 1 and cell.has_wall(Wall.SOUTH):
                    # Render coordinates of horizontal wall
                    wall_x = 2 * x + 1
                    wall_y = 2 * y + 2
                    if (wall_x, wall_y) not in forbidden:
                        if (self.is_valid(x, y + 1) and
                            not self._would_create_2x2_block(
                                x, y, Wall.SOUTH)):
                            valid_candidates.append(
                                (x, y, Wall.SOUTH, x, y + 1)
                            )

                # Check east wall
                if x < self.width - 1 and cell.has_wall(Wall.EAST):
                    # Render coordinates of vertical wall
                    wall_x = 2 * x + 2
                    wall_y = 2 * y + 1
                    if (wall_x, wall_y) not in forbidden:
                        if (self.is_valid(x + 1, y) and
                            not self._would_create_2x2_block(
                                x, y, Wall.EAST)):
                            valid_candidates.append(
                                (x, y, Wall.EAST, x + 1, y)
                            )

        # Shuffle and remove walls
        random.shuffle(valid_candidates)
        for i, (x1, y1, wall, x2, y2) in enumerate(
            valid_candidates
        ):
            if i >= loops:
                break
            self.remove_wall_between(x1, y1, x2, y2)

    def _would_create_2x2_block(
            self, x: int, y: int, wall_removed: Wall
    ) -> bool:
        """
        Check if removing a wall would create a 2x2 block of
        completely open cells.
        """
        check_offsets = []
        if wall_removed == Wall.SOUTH:
            check_offsets = [(0, 0), (-1, 0)]
        elif wall_removed == Wall.EAST:
            check_offsets = [(0, 0), (0, -1)]

        for ox, oy in check_offsets:
            # Base x,y for a 2x2 block (top-left corner)
            bx, by = x + ox, y + oy
            if 0 <= bx < self.width - 1 and 0 <= by < self.height - 1:
                # Count open internal walls in this 2x2 block
                open_walls = 0
                # Check internal walls of the 2x2 block:
                if not self.cells[by][bx].has_wall(Wall.EAST):
                    open_walls += 1
                if not self.cells[by][bx].has_wall(Wall.SOUTH):
                    open_walls += 1
                if not self.cells[by][bx + 1].has_wall(Wall.SOUTH):
                    open_walls += 1
                if not self.cells[by + 1][bx].has_wall(Wall.EAST):
                    open_walls += 1

                if open_walls >= 3:
                    return True
        return False

    def __repr__(self) -> str:
        """String representation of maze."""
        return f"Maze({self.width} x {self.height})"
