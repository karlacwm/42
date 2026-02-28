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
        return [
            Direction.NORTH, Direction.EAST,
            Direction.SOUTH, Direction.WEST
        ]

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

    def get_neighbors(
            self, x: int, y: int
    ) -> List[Tuple[int, int, Tuple[int, int]]]:
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

    def add_loops(
            self,
            forbidden: Tuple[int, int],
            loops: int
    ) -> None:
        """
        Add loops to a perfect maze by removing internal walls.

        This creates cycles in the maze structure while respecting
        constraints:
        - Only removes internal walls (not outer borders)
        - Never removes forbidden walls (e.g., "42" pattern)
        - Prevents creation of 2x2 blocks of completely open cells
        - Preserves structural integrity

        Args:
            forbidden: Set of (render_x, render_y) coordinates
                      that must not be removed
            loops: Maximum number of walls to remove
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
            self, x: int, y: int, wall: Wall
    ) -> bool:
        """
        Check if removing a wall would create a 2x2 block of
        completely open cells.

        A 2x2 block is when 4 cells have no internal walls between
        them.

        Args:
            x, y: Cell coordinates
            wall: Wall to check (SOUTH or EAST)

        Returns:
            True if removing wall would complete a 2x2 block
        """
        if wall == Wall.SOUTH:
            # Wall is between (x, y) and (x, y+1)
            # Check both possible 2x2 blocks
            for bx in [x - 1, x]:
                if 0 <= bx < self.width - 1:
                    block = [
                        (bx, y), (bx + 1, y),
                        (bx, y + 1), (bx + 1, y + 1)
                    ]
                    if all(self.is_valid(*c) for c in block):
                        if self._would_complete_2x2(block):
                            return True

        elif wall == Wall.EAST:
            # Wall is between (x, y) and (x+1, y)
            # Check both possible 2x2 blocks
            for by in [y - 1, y]:
                if 0 <= by < self.height - 1:
                    block = [
                        (x, by), (x + 1, by),
                        (x, by + 1), (x + 1, by + 1)
                    ]
                    if all(self.is_valid(*c) for c in block):
                        if self._would_complete_2x2(block):
                            return True

        return False

    def _would_complete_2x2(
            self, block: List[Tuple[int, int]]
    ) -> bool:
        """
        Check if a 2x2 block already has 3 of 4 internal walls open.

        This indicates that removing one more wall would create
        a completely open 2x2 block.

        Args:
            block: List of 4 cell coordinates in 2x2 arrangement

        Returns:
            True if block would become completely open
        """
        block = sorted(block)  # Ensure consistent order
        bx, by = block[0]

        c00 = self.get_cell(bx, by)
        c10 = self.get_cell(bx + 1, by)
        c01 = self.get_cell(bx, by + 1)
        # c11 = self.get_cell(bx + 1, by + 1)

        # Count how many internal walls are already open
        walls_open = 0
        if not c00.has_wall(Wall.EAST):
            walls_open += 1
        if not c00.has_wall(Wall.SOUTH):
            walls_open += 1
        if not c10.has_wall(Wall.SOUTH):
            walls_open += 1
        if not c01.has_wall(Wall.EAST):
            walls_open += 1

        # If 3 are already open, removing the 4th would complete it
        return walls_open >= 3

    def __repr__(self) -> str:
        """String representation of maze."""
        return f"Maze({self.width}x{self.height})"
