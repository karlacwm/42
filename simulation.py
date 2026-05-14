from dataclasses import dataclass
from network import Zone, Network, Connection, ZoneType, connection_pair
from typing import Optional


@dataclass
class Drone:
    drone_id: str
    current_zone: Zone
    path: list[Zone]
    path_tracking: int = 0
    cooldown: int = 0
    finished: bool = False

    def find_next_zone(self) -> Optional[Zone]:
        if self.path_tracking + 1 < len(self.path):
            return self.path[self.path_tracking + 1]
        return None

    def __post_init__(self) -> None:
        if self.current_zone:
            self.current_zone.current_drones.append(self)


class Simulation:
    def __init__(self, network: Network, drones: list[Drone]) -> None:
        self.network = network
        self.drones = drones
        self.turn_number = 0
        self.history: list[dict[str, str]] = []

    def record_history(self) -> None:
        snapshot = {
            drone.drone_id: drone.current_zone.name for drone in self.drones
        }
        self.history.append(snapshot)

    def run(self) -> None:
        """The main loop. Keeps running until all drones are done."""
        self.record_history()
        while not self.all_drones_finished():
            self.turn_number += 1
            self.play_turn()
            self.record_history()

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

    def drone_sort_key(self, drone: Drone) -> tuple[bool, int, int]:
        digits = "".join(char for char in drone.drone_id if char.isdigit())
        number = int(digits) if digits else 0
        remaining_distance = len(drone.path) - drone.path_tracking
        return (
            drone.finished,
            remaining_distance,  # Prioritize drones closest to finish
            number,
        )

    def play_turn(self) -> int:
        """The traffic cop logic for a single step of time."""
        traffic_this_turn = {
            connection_pair(conn.zone1, conn.zone2): 0
            for conn in self.network.connections
        }

        moves_output = []

        self.drones.sort(key=self.drone_sort_key)

        for drone in self.drones:
            if drone.finished:
                continue

            if drone.cooldown > 0:
                drone.cooldown -= 1
                continue

            next_zone = drone.find_next_zone()
            if not next_zone:
                continue

            conn = self.get_connection(drone.current_zone, next_zone)
            if not conn:
                continue

            conn_key = connection_pair(conn.zone1, conn.zone2)

            if traffic_this_turn[conn_key] >= conn.max_link_capacity:
                continue

            if next_zone != self.network.end_hub:
                if self.drones_in_zone(next_zone) >= next_zone.max_drones:
                    continue

            try:
                drone.current_zone.current_drones.remove(drone)
            except ValueError:
                pass

            drone.current_zone = next_zone
            drone.path_tracking += 1
            next_zone.current_drones.append(drone)

            traffic_this_turn[conn_key] += 1

            if next_zone.zone_type == ZoneType.restricted:
                drone.cooldown = 1

            if next_zone == self.network.end_hub:
                drone.finished = True

            moves_output.append(f"{drone.drone_id}-{next_zone.name}")

        if moves_output:
            print(" ".join(moves_output))

        return len(moves_output)

# note to self
# is the drone on cooldown?
# what is the drone's next zone? get from pathfinder
# find conn between the current zone and the next zone
# check connection capacity, current turn traffic?
# check zone cap, current zone and next zone
# (but the drone in next zone will also move)
# if all checks pass -> move the drone, update capacities
# and add to moves_output

# remember docstrings
