"""Common utilities for the mazegen package."""
from typing import Set, Tuple


def get_pattern_cells(width: int, height: int) -> Set[Tuple[int, int]]:
    """
    Returns a set of (x, y) coordinates that form the '42' pattern.
    This is the Single Source of Truth for the pattern location.
    """
    if width < 12 or height < 10:
        return set()

    coords = set()
    cx, cy = width // 2, height // 2

    # Relative offsets
    digit_4 = {
        (0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (2, 4)
    }
    digit_2 = {
        (0, 0), (1, 0), (2, 0), (2, 1), (0, 2), (1, 2), (2, 2),
        (0, 3), (0, 4), (1, 4), (2, 4)
    }

    start_x = cx - 3
    start_y = cy - 2

    for dx, dy in digit_4:
        coords.add((start_x + dx, start_y + dy))
    for dx, dy in digit_2:
        coords.add((start_x + 4 + dx, start_y + dy))

    return coords
