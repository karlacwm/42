import sys
from parser import MapParser, ParseError
from visualiser import Visualiser
from pathfinder import Pathfinder


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <map_file.txt>")
        sys.exit(1)

    filepath = sys.argv[1]

    parser = MapParser(filepath)

    try:
        parser.parse()
        print(f"Success! Parsed map with {parser.drones_total} drones.")

        # visual = Visualiser(network=parser.network,
        #                     canvas_w=1600, parser=parser,
        #                     canvas_h=1000, padding=80)
        # visual.visualise()

        solver = Pathfinder(network=parser.network)
        solver.find_path()

    except ParseError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e.__class__}: {e}")


if __name__ == "__main__":
    main()
