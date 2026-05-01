from dataclasses import dataclass
from os import path
from network import Zone, Network


@dataclass
class Drone:
    drone_id: int
    current_zone: Zone
    cooldown: int
    path: list[Zone]
    path_tracking: int = 0
    finished: bool = False


class Simulation:
    def __init__(self, network: Network, drones: list[Drone]) -> None:
        self.network = network
        self.drones = drones
        self.turn_number = 0

    def run(self) -> None:
        """The main loop. Keeps running until all drones are done."""
        while not self.all_drones_finished():
            self.turn_number += 1
            self.play_turn()

    def all_drones_finished(self) -> bool:
        """Checks if every drone has reached the end_hub."""
        for drone in self.drones:
            if not drone.finished:
                return False
        return True

    def play_turn(self) -> None:
        """The traffic cop logic for a single step of time."""
        traffic_this_turn = {conn: 0 for conn in self.network.connections}

        moves_output = []

        for drone in self.drones:
            if drone.finished:
                continue

            if drone.cooldown > 0:
                drone.cooldown -= 1
            else:
                drone.current_zone = drone.path[drone.path_tracking + 1]






        if moves_this_turn:
            print(" ".join(moves_this_turn))

            #  Is the drone on cooldown? (Reduce timer and skip if yes)

            # What is the drone's next zone?

            # Find the connection between the current zone and the next zone

            # Check Connection Capacity (Using current_turn_traffic)

            # Check Zone Capacity (Are there too many drones currently sitting in the next zone?)

            # If all checks pass -> Move the drone, update capacities, and add to moves_this_turn!
            pass
