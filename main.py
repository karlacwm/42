import sys
from parser import MapParser
from pathfinder import Pathfinder
from engine import SimulationEngine, Drone
from visualiser import Visualiser


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <map_file.txt>")
        sys.exit(1)

    filepath = sys.argv[1]
    parser = MapParser(filepath)
    parser.parse()
    network = parser.network

    if not network.start_hub or not network.end_hub:
        print("Error: Missing start or end hub.")
        return

    pathfinder = Pathfinder(network)
    path = pathfinder.find_shortest_path(network.start_hub, network.end_hub)

    if not path:
        print("No path found!")
        return

    drones = [Drone(f"D{i+1}", network.start_hub, path)
              for i in range(parser.drones_total)]

    print("Running Simulation...")
    engine = SimulationEngine(network, drones)
    engine.run_simulation()

    print(f"Simulation finished in {engine.turn_number} turns!")

    viz = Visualiser(
        network,
        canvas_w=1800,
        canvas_h=1200,
        padding=70,
        map_filepath=filepath,
    )
    viz.visualise(engine.history)


if __name__ == "__main__":
    main()
