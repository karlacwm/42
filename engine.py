from network import Network, Zone
from typing import List, Dict


class Drone:
    def __init__(self, drone_id: str, start_zone: Zone, path: List[Zone]) -> None:
        self.id = drone_id
        self.current_zone = start_zone
        self.path = path  # The list of zones it needs to visit
        self.path_index = 0  # Where it currently is on that path

        # Add the drone to the starting zone's capacity
        self.current_zone.current_drones.append(self)

    def get_next_zone(self) -> Zone | None:
        """Returns the next zone on the path, or None if it has reached the end."""
        if self.path_index + 1 < len(self.path):
            return self.path[self.path_index + 1]
        return None


class SimulationEngine:
    def __init__(self, network: Network, drones: List[Drone]) -> None:
        self.network = network
        self.drones = drones
        self.turn_number = 0
        self.history: List[Dict[str, str]] = []  # For the Visualiser

    def run_simulation(self) -> None:
        """Runs the loop until all drones finish."""
        # Save the initial state for Turn 0
        self._record_history()

        # Keep running until all drones are at the end hub
        while not self._all_drones_finished():
            self.turn_number += 1
            self._play_one_turn()
            self._record_history()

    def _play_one_turn(self) -> None:
        """The core logic for a single step of time."""
        # 1. Reset link traffic for this turn
        link_usage: Dict[tuple[str, str], int] = {}
        for conn in self.network.connections:
            key = self._connection_key(conn.zone1, conn.zone2)
            link_usage[key] = 0

        # A list to store the official output strings for this turn (e.g., "D1-roof1")
        turn_output = []

        # 2. Process every drone
        for drone in self.drones:
            next_zone = drone.get_next_zone()

            # If the drone is already at the end, skip it
            if not next_zone:
                continue

            # Find the connection between where the drone is, and where it wants to go
            connection = self._find_connection(drone.current_zone, next_zone)
            if not connection:
                continue  # Should never happen if pathfinder works!

            # --- THE BOUNCER CHECKS ---
            # Check 1: Is the connection overloaded this turn?
            connection_key = self._connection_key(
                connection.zone1,
                connection.zone2,
            )
            if link_usage[connection_key] >= connection.max_link_capacity:
                continue  # Drone must wait

            # Check 2: Is the target zone full right now?
            if next_zone.is_full:
                continue  # Drone must wait

            # --- MOVE THE DRONE ---
            # Remove from old zone
            drone.current_zone.current_drones.remove(drone)

            # Move to new zone
            drone.current_zone = next_zone
            drone.path_index += 1
            next_zone.current_drones.append(drone)

            # Update the traffic for this turn
            link_usage[connection_key] += 1

            # Format the output required by the project!
            turn_output.append(f"{drone.id}-{drone.current_zone.name}")

        # If any drones moved, print the official turn string
        if turn_output:
            print(" ".join(turn_output))

    # --- Helper Methods ---

    def _connection_key(self, z1: Zone, z2: Zone) -> tuple[str, str]:
        """Returns a stable key for an undirected connection."""
        if z1.name <= z2.name:
            return z1.name, z2.name
        return z2.name, z1.name

    def _find_connection(self, z1: Zone, z2: Zone):
        """Looks up the connection object between two zones."""
        for conn in self.network.connections:
            if (conn.zone1 == z1 and conn.zone2 == z2) or (conn.zone1 == z2 and conn.zone2 == z1):
                return conn
        return None

    def _all_drones_finished(self) -> bool:
        """Checks if every single drone is sitting in the end_hub."""
        for drone in self.drones:
            if drone.current_zone != self.network.end_hub:
                return False
        return True

    def _record_history(self) -> None:
        """Saves positions so the Tkinter visualiser can replay the turns."""
        state = {drone.id: drone.current_zone.name for drone in self.drones}
        self.history.append(state)
