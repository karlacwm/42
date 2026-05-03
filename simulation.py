from dataclasses import dataclass
from network import Zone, Network, Connection
from typing import Optional


@dataclass
class Drone:
    drone_id: int
    current_zone: Zone
    cooldown: int
    path: list[Zone]
    path_tracking: int = 0
    finished: bool = False

    def find_next_zone(self) -> Optional[Zone]:
        if self.path_tracking + 1 < len(self.path):
            return self.path[self.path_tracking + 1]
        return None


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

    def get_connection(self, z1: Zone, z2: Zone) -> Optional[Connection]:
        for conn in self.network.connections:
            if (conn.zone1 == z1 and conn.zone2 == z2) or \
                    (conn.zone1 == z2 and conn.zone2 == z1):
                return conn
        return None

    def drones_in_zone(self, zone: Zone) -> int:
        count = 0
        for drone in self.drones:
            if drone.current_zone == zone and not drone.finished:
                count += 1
        return count

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

            next_zone = drone.find_next_zone()
            if not next_zone:
                continue

            conn = self.get_connection(drone.current_zone, next_zone)
            if not conn:
                continue

            if self.drones_in_zone(drone.current_zone) < drone.current_zone.max_drones:
                

        if moves_output:
            print(" ".join(moves_output))

# note to self
# is the drone on cooldown?
# what is the drone's next zone? get from pathfinder
# find conn between the current zone and the next zone
# check connection capacity, current turn traffic?
# check zone cap, current zone and next zone
# (but the drone in next zone will also move)
# if all checks pass -> move the drone, update capacities
# and add to moves_output
