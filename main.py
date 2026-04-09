import sys
from parser import MapParser, ParseError


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <map_file>")
        sys.exit(1)

    filepath = sys.argv[1]

    try:


if __name__ == "__main__":
    main()
