"""Maze data structures and wall encoding."""
from typing import List, Tuple
from enum import IntFlag


class Wall(IntFlag):
    """
    Wall encoding using bits 0-3 for N, E, S, W directions.

    Bit 0 (0x1): North wall
    Bit 1 (0x2): East wall
    Bit 2 (0x4): South wall
    Bit 3 (0x8): West wall
    """
    NORTH = 0x1  # Bit 0
    EAST = 0x2   # Bit 1
    SOUTH = 0x4  # Bit 2
    WEST = 0x8   # Bit 3
    ALL = 0xF    # All walls


class Direction:
    """Direction constants for maze navigation."""
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)

    @staticmethod
    def all() -> List[Tuple[int, int]]:
        """Return all directions."""
        return [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]

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
        else:
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
        Initialize a cell.

        Args:
            x: X coordinate
            y: Y coordinate
        """
        self.x = x
        self.y = y
        self.walls = Wall.ALL  # Start with all walls

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
        return f"Cell({self.x}, {self.y}, walls=0x{self.walls:X})"


class Maze:
    """Represents a maze grid."""

    def __init__(self, width: int, height: int) -> None:
        """
        Initialize a maze.

        Args:
            width: Width of the maze
            height: Height of the maze
        """
        self.width = width
        self.height = height
        self.cells: List[List[Cell]] = []

        # Initialize grid
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

    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int, Tuple[int, int]]]:
        """
        Get valid neighbors of a cell.

        Returns:
            List of tuples (nx, ny, direction) for each valid neighbor
        """
        neighbors = []
        for direction in Direction.all():
            dx, dy = direction
            nx, ny = x + dx, y + dy
            if self.is_valid(nx, ny):
                neighbors.append((nx, ny, direction))
        return neighbors

    def remove_wall_between(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """
        Remove wall between two adjacent cells.

        Args:
            x1, y1: Coordinates of first cell
            x2, y2: Coordinates of second cell
        """
        # Calculate direction from cell1 to cell2
        dx = x2 - x1
        dy = y2 - y1
        direction = (dx, dy)

        # Remove wall from first cell
        wall1 = Direction.to_wall(direction)
        self.cells[y1][x1].remove_wall(wall1)

        # Remove opposite wall from second cell
        opposite_dir = Direction.opposite(direction)
        wall2 = Direction.to_wall(opposite_dir)
        self.cells[y2][x2].remove_wall(wall2)

    def to_hex_grid(self) -> List[List[str]]:
        """
        Convert maze to hexadecimal grid representation.

        Returns:
            2D list of hex strings representing wall states
        """
        hex_grid = []
        for row in self.cells:
            hex_row = [cell.to_hex() for cell in row]
            hex_grid.append(hex_row)
        return hex_grid

    # def start(self)

    def __repr__(self) -> str:
        """String representation of maze."""
        return f"Maze({self.width}x{self.height})"
