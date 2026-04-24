import sys
from parser import MapParser, ParseError
from visualiser import Visualiser


def main() -> None:
    # Ensure the user provides a map file
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <map_file.txt>")
        sys.exit(1)

    filepath = sys.argv[1]

    # 1. Initialize your Parser
    parser = MapParser(filepath)

    try:
        # 2. Parse the file
        parser.parse()
        print(f"Success! Parsed map with {parser.drones_total} drones.")

        # 3. Pass the parsed Network to the Visualizer
        viz = Visualiser(network=parser.network,
                         canvas_w=1600, parser=parser,
                         canvas_h=1000, padding=80)
        viz.visualise()

    except ParseError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
