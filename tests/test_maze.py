"""Tests for maze module."""
from mazegen.maze import Maze, Cell, Wall, Direction


def test_cell_initialization() -> None:
    """Test cell initialization."""
    cell = Cell(0, 0)
    assert cell.x == 0
    assert cell.y == 0
    assert cell.walls == Wall.ALL


def test_cell_remove_wall() -> None:
    """Test removing walls from cell."""
    cell = Cell(0, 0)
    cell.remove_wall(Wall.NORTH)
    assert not cell.has_wall(Wall.NORTH)
    assert cell.has_wall(Wall.EAST)
    assert cell.has_wall(Wall.SOUTH)
    assert cell.has_wall(Wall.WEST)


def test_cell_to_hex() -> None:
    """Test cell hex representation."""
    cell = Cell(0, 0)
    assert cell.to_hex() == 'F'

    cell.remove_wall(Wall.NORTH)
    assert cell.to_hex() == 'E'

    cell.remove_wall(Wall.EAST)
    assert cell.to_hex() == 'C'


def test_maze_initialization() -> None:
    """Test maze initialization."""
    maze = Maze(5, 5)
    assert maze.width == 5
    assert maze.height == 5
    assert len(maze.cells) == 5
    assert len(maze.cells[0]) == 5


def test_maze_get_cell() -> None:
    """Test getting cell from maze."""
    maze = Maze(3, 3)
    cell = maze.get_cell(1, 1)
    assert cell.x == 1
    assert cell.y == 1


def test_maze_is_valid() -> None:
    """Test coordinate validation."""
    maze = Maze(3, 3)
    assert maze.is_valid(0, 0)
    assert maze.is_valid(2, 2)
    assert not maze.is_valid(-1, 0)
    assert not maze.is_valid(0, -1)
    assert not maze.is_valid(3, 0)
    assert not maze.is_valid(0, 3)


def test_maze_get_neighbors() -> None:
    """Test getting cell neighbors."""
    maze = Maze(3, 3)

    # Corner cell (0, 0) should have 2 neighbors
    neighbors = maze.get_neighbors(0, 0)
    assert len(neighbors) == 2

    # Center cell (1, 1) should have 4 neighbors
    neighbors = maze.get_neighbors(1, 1)
    assert len(neighbors) == 4


def test_maze_remove_wall_between() -> None:
    """Test removing wall between cells."""
    maze = Maze(3, 3)

    # Remove wall between (0, 0) and (1, 0)
    maze.remove_wall_between(0, 0, 1, 0)

    cell1 = maze.get_cell(0, 0)
    cell2 = maze.get_cell(1, 0)

    assert not cell1.has_wall(Wall.EAST)
    assert not cell2.has_wall(Wall.WEST)


def test_maze_to_hex_grid() -> None:
    """Test converting maze to hex grid."""
    maze = Maze(2, 2)
    hex_grid = maze.to_hex_grid()

    assert len(hex_grid) == 2
    assert len(hex_grid[0]) == 2
    assert all(cell == 'F' for row in hex_grid for cell in row)


def test_direction_all() -> None:
    """Test getting all directions."""
    directions = Direction.all()
    assert len(directions) == 4
    assert Direction.NORTH in directions
    assert Direction.EAST in directions
    assert Direction.SOUTH in directions
    assert Direction.WEST in directions


def test_direction_to_wall() -> None:
    """Test converting direction to wall."""
    assert Direction.to_wall(Direction.NORTH) == Wall.NORTH
    assert Direction.to_wall(Direction.EAST) == Wall.EAST
    assert Direction.to_wall(Direction.SOUTH) == Wall.SOUTH
    assert Direction.to_wall(Direction.WEST) == Wall.WEST


def test_direction_opposite() -> None:
    """Test getting opposite direction."""
    assert Direction.opposite(Direction.NORTH) == Direction.SOUTH
    assert Direction.opposite(Direction.EAST) == Direction.WEST
    assert Direction.opposite(Direction.SOUTH) == Direction.NORTH
    assert Direction.opposite(Direction.WEST) == Direction.EAST


def test_wall_encoding() -> None:
    """Test wall encoding values."""
    assert Wall.NORTH == 0x1
    assert Wall.EAST == 0x2
    assert Wall.SOUTH == 0x4
    assert Wall.WEST == 0x8
    assert Wall.ALL == 0xF
