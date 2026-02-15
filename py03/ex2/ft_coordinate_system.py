import sys
import math


def calculate_distance(p1: tuple[int, int, int],
                       p2: tuple[int, int, int]) -> float:
    '''
    Calculates distance between two coordinates.
    '''
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


def parse_coordinate(p1: str) -> tuple[int, int, int] | None:
    '''
    Parses coordinates and splits them from a string if it is valid.
    '''
    try:
        pos: list[str] = p1.split(",")
        if len(pos) != 3:
            raise IndexError(
                "Coordinates must have exactly 3 values \"x,y,z\"")
        x: int = int(pos[0])
        y: int = int(pos[1])
        z: int = int(pos[2])
        return x, y, z
    except (IndexError, ValueError) as e:
        print("Error parsing coordinates:", e)
        print(f"Error details - Type: {type(e).__name__}, Args: {e.args}")
        print()
        return None


def coordinate_system() -> None:
    '''
    Parses coordinates, calculates distances and shows player's location.
    '''
    print("=== Game Coordinate System ===", end="\n\n")
    start: tuple[int, int, int] = (0, 0, 0)
    pos: tuple[int, int, int] = (10, 20, 5)
    distance: float = calculate_distance(start, pos)
    print(f"Position created: {pos}")
    print(f"Distance between {start} and {pos}: {distance:.2f}")
    print()
    pos_str: str = "3,4,0"
    print(f"Parsing coordinates: \"{pos_str}\"")
    parsed: tuple[int, int, int] | None = parse_coordinate(pos_str)
    if parsed is not None:
        x1, y1, z1 = parsed
        distance1: float = calculate_distance(start, parsed)
        print(f"Parsed position: {parsed}")
        print(f"Distance between {start} and {parsed}: {distance1:.2f}")
        print()
    pos_bad: str = "abc,def,ghi"
    print(f"Parsing invalid coordinates: \"{pos_bad}\"")
    parse_coordinate(pos_bad)
    if len(sys.argv) == 2:
        pos_argv: str = sys.argv[1]
        print(f"Parsing coordinates from command line: \"{pos_argv}\"")
        parsed_argv: tuple[int, int, int] | None = parse_coordinate(pos_argv)
        if parsed_argv is not None:
            x2, y2, z2 = parsed_argv
            print(f"Parsed position: {parsed_argv}")
            distance_argv: float = calculate_distance(start, parsed_argv)
            print(f"Distance between {start} and {parsed_argv}:"
                  f" {distance_argv:.2f}")
            print()
            print("Unpacking demonstration:")
            print(f"Player at x={x2}, y={y2}, z={z2}")
            print(f"Coordinates: X={x2}, Y={y2}, Z={z2}")
    else:
        if parsed is not None:
            print("Unpacking demonstration:")
            print(f"Player at x={x1}, y={y1}, z={z1}")
            print(f"Coordinates: X={x1}, Y={y1}, Z={z1}")


if __name__ == "__main__":
    coordinate_system()
