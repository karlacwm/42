import sys
from parser import MapParser, ParseError
from visualiser import Visualiser
from pathfinder import Pathfinder
from simulation import Simulation, Drone
from network import connection_pair


def main() -> None:
    if len(sys.argv) != 2:
        print("Try again with:\npython3 main.py <map_file.txt>\n\n"
              "OR choose a map file in Makefile and run \"make run\"")
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

        for index in range(parser.drones_total):
            path = solver.find_path(traffic)
            if not path:
                print(f"Error: Could not find a path for D{index + 1}!")
                return

            drone = Drone(
                drone_id=f"D{index + 1}",
                current_zone=network.start_hub,
                path=path,
            )
            all_drones.append(drone)

            for current_zone, next_zone in zip(path, path[1:]):
                edge_key = connection_pair(current_zone, next_zone)
                traffic[edge_key] = traffic.get(edge_key, 0) + 1

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
