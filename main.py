import sys
from mapparser import MapParser, ParseError


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <map_file>")
        sys.exit(1)

    filepath = sys.argv[1]

    try:
        # Initialize parser and parse the file
        parser = MapParser(filepath)
        graph, nb_drones = parser.parse()

        # Print the results to verify
        print(f"Successfully parsed map: {filepath}")
        print(f"Total Drones: {nb_drones}")
        print(f"Start Hub: {graph.start_hub}")
        print(f"End Hub: {graph.end_hub}")

        print("\nAll Zones:")
        for name, zone in graph.zones.items():
            print(f"  - {zone}")

        print("\nAll Connections:")
        for conn in graph.connections:
            print(f"  - {conn}")

    except ParseError as e:
        print(f"Failed to parse map:\n{e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
