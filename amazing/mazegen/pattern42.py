"""
Gets the pattern 42 location with the cell coordinates.
"""
from typing import Set, Tuple


def get_pattern_cells(width: int, height: int) -> Set[Tuple[int, int]]:
    """
    Returns a set of (x, y) coordinates that form the '42' pattern.
    """
    if width < 12 or height < 10:
        return set()

    coords: set[Tuple[int, int]] = set()
    cx, cy = width // 2, height // 2

    digit_4 = {
        (0, 0), (0, 1), (0, 2),
        (1, 2),
        (2, 2), (2, 3), (2, 4)
    }
    digit_2 = {
        (0, 0), (1, 0), (2, 0),
        (2, 1),
        (0, 2), (1, 2), (2, 2),
        (0, 3),
        (0, 4), (1, 4), (2, 4)
    }

    start_x = cx - 3
    start_y = cy - 2

    coords.update((start_x + dx, start_y + dy) for dx, dy in digit_4)
    digit_2_start_x = start_x + 4
    coords.update((digit_2_start_x + dx, start_y + dy) for dx, dy in digit_2)

    return coords
