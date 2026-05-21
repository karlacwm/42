"""Simulation primitives: Drone and Simulation runner."""

from dataclasses import dataclass
from network import Zone, Network, Connection, ZoneType, connection_pair
from typing import Optional


@dataclass
class Drone:
    """A drone with its id, position, planned path and movement state."""

    drone_id: str
    current_zone: Zone
    path: list[Zone]
    path_tracking: int = 0
    cooldown: int = 0
    finished: bool = False

    def find_next_zone(self) -> Optional[Zone]:
        """Return the next zone on the drone's path or None if at end."""

        if self.path_tracking + 1 < len(self.path):
            return self.path[self.path_tracking + 1]
        return None

    def __post_init__(self) -> None:
        """Register the drone in its current zone's occupancy list."""

        if self.current_zone:
            self.current_zone.current_drones.append(self)


class Simulation:
    """Discrete-step simulation of drones moving through the Network."""

    def __init__(self, network: Network, drones: list[Drone]) -> None:

        # def __init__(self, network: Network, drones: list[Drone], cap: bool
        #              ) -> None:
        """Create a Simulation with a network and participating drones."""

        self.network = network
        self.drones = drones
        self.turn_number = 0
        self.history: list[dict[str, str]] = []
        # self.cap = cap
        self.turn_traffic: dict[tuple[str, str], int] = {}

    def record_history(self) -> None:
        """Append a snapshot of drones' current zones to the history."""

        snapshot = {
            drone.drone_id: drone.current_zone.name for drone in self.drones
        }
        self.history.append(snapshot)

    def run(self) -> None:
        """Run turns until all drones have finished their paths."""
        self.record_history()
        while not self.all_drones_finished():
            self.turn_number += 1
            self.play_turn()
            self.record_history()

    def all_drones_finished(self) -> bool:
        """Return True when all drones have reached the end hub."""
        for drone in self.drones:
            if not drone.finished:
                return False
        return True

    def get_connection(self, z1: Zone, z2: Zone) -> Optional[Connection]:
        """Return the Connection linking z1 and z2, or None if none."""

        for conn in self.network.connections:
            if (conn.zone1 == z1 and conn.zone2 == z2) or \
                    (conn.zone1 == z2 and conn.zone2 == z1):
                return conn
        return None

    def drone_sort_key(self, drone: Drone) -> tuple[bool, int, int]:
        """Sorting key for prioritising drone moves each turn."""

        digits = "".join(char for char in drone.drone_id if char.isdigit())
        number = int(digits) if digits else 0
        remaining_distance = len(drone.path) - drone.path_tracking
        return (
            drone.finished,
            remaining_distance,
            number,
        )

    def play_turn(self) -> int:
        """Execute one simulation turn and return number of moves made."""
        traffic_this_turn = {
            connection_pair(conn.zone1, conn.zone2): 0
            for conn in self.network.connections
        }
        self.turn_traffic = traffic_this_turn

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
                if len(next_zone.current_drones) >= next_zone.max_drones:
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

        # if self.cap:
        #     self.print_cap_info()

        return len(moves_output)

    # def print_cap_info(self) -> None:
    #     print("Capacity info:")

    #     for zone in self.network.zones.values():
    #         if "start" in zone.name or "goal" in zone.name:
    #             print(f"Zone {zone.name}: "
    #                   f"{len(zone.current_drones)}/- drones")
    #         else:
    #             print(
    #                 f"Zone {zone.name}: "
    #                 f"{len(zone.current_drones)}/{zone.max_drones} drones"
    #             )

    #     for conn in self.network.connections:
    #         key = connection_pair(conn.zone1, conn.zone2)
    #         print(
    #             f"Connection {conn.zone1.name}-{conn.zone2.name}: "
    #             f"{self.traffic[key]}/"
    #             f"{conn.max_link_capacity} capacity used"
    #         )

    #     print()

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
