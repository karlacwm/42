import sys
from parser import MapParser, ParseError
from pathfinder import Pathfinder
from engine import SimulationEngine, Drone
from visualiser import Visualiser


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <map_file.txt>")
        sys.exit(1)

    try:
        filepath = sys.argv[1]
        parser = MapParser(filepath)
        parser.parse()
        network = parser.network

        pathfinder = Pathfinder(network)
        path = pathfinder.find_shortest_path(
            network.start_hub, network.end_hub)

        if not path:
            print("No path found!")
            return

        drones = [Drone(f"D{i+1}", network.start_hub, path)
                  for i in range(parser.drones_total)]

        print("Running Simulation...")
        engine = SimulationEngine(network, drones)
        engine.run_simulation()

        print(f"Simulation finished in {engine.turn_number} turns!")

        flyin = Visualiser(
            network,
            canvas_w=1800,
            canvas_h=1200,
            padding=70,
            map_filepath=filepath,
        )
        flyin.visualise(engine.history)
    except FileNotFoundError as e:
        print(e)
    except ParseError as e:
        print(e)
    except Exception as e:
        print(f"Caught an unexpected error: {e}")


if __name__ == "__main__":
    main()
