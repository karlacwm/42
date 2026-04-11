import sys
from parser import MapParser, ParseError
from visualiser import Visualiser


def main() -> None:
    if len(sys.argv) != 2:
        print("Please run with the format: python3 main.py <map_file>")
        sys.exit(1)

    filepath = sys.argv[1]

    try:

        parser = MapParser(filepath=filepath)
        parser.parse()
        print(parser.network)

        testing = Visualiser(network=parser.network, canvas_w=1700,
                             canvas_h=1200, padding=60)
        testing.visualise()
    except ParseError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Caught an unexpected error: {e}")


if __name__ == "__main__":
    main()
