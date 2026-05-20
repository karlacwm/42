"""Parse map, run simulation and visualise results."""

import sys
from parser import MapParser, ParseError
from visualiser import Visualiser
from pathfinder import Pathfinder
from simulation import Simulation, Drone


def main() -> None:
    """Entry point: parse a map, run the simulation, and visualise."""

    if len(sys.argv) != 2:
        print("Try again with:\npython3 main.py <map_file.txt>\n\n"
              "OR\nmake run <map_file.txt>")
        sys.exit(1)

    filepath = sys.argv[1]

    try:
        parser = MapParser(filepath)
        parser.parse()
        print(f"Success! Parsed map with {parser.drones_total} drones.")

        network = parser.network
        if not network.start_hub or not network.end_hub:
            print("Error: start_hub or end_hub missing from map.")
            return

        solver = Pathfinder(network=network)
        traffic: dict[tuple[str, str], int] = {}
        all_drones: list[Drone] = []
        best_count = 2

        for index in range(parser.drones_total):
            paths = solver.dynamic_pathfinder(parser.drones_total, traffic)
            if not paths:
                print(f"Error: Could not find a path for D{index + 1}!")
                return

            drone = Drone(
                drone_id=f"D{index + 1}",
                current_zone=network.start_hub,
                path=paths[index % best_count],
            )
            all_drones.append(drone)

        print("\n--- SIMULATION OUTPUT ---")
        sim = Simulation(network, all_drones)
        sim.run()
        print(f"\nFinished in {sim.turn_number} turns ٩(ˊᗜ ˋ)و")

        visual = Visualiser(network=network,
                            canvas_w=1600, parser=parser,
                            canvas_h=1000, padding=80,
                            history=sim.history)
        visual.visualise()

    except ParseError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e.__class__}: {e}")


if __name__ == "__main__":
    main()
