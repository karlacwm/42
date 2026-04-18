from network import Network, Zone
from typing import List, Optional


class Pathfinder:
    def __init__(self, network: Network) -> None:
        self.network = network

    def get_neighbors(self, current_zone: Zone) -> List[Zone]:
        """Finds all zones connected to the current zone."""
        neighbors = []
        for conn in self.network.connections:
            if conn.zone1.name == current_zone.name:
                neighbors.append(conn.zone2)
            elif conn.zone2.name == current_zone.name:
                neighbors.append(conn.zone1)
        return neighbors

    def find_shortest_path(self, start: Zone, end: Zone) -> Optional[List[Zone]]:
        """A simple Breadth-First Search (BFS) to find the shortest path."""
        # A queue to keep track of paths we are exploring
        queue = [[start]]

        # A set to keep track of zones we have already visited
        visited = set([start.name])

        while queue:
            # Get the first path from the queue
            current_path = queue.pop(0)
            # Get the last zone in that path
            current_zone = current_path[-1]

            # If we reached the end, we found our path!
            if current_zone.name == end.name:
                return current_path

            # Otherwise, check all neighboring zones
            for neighbor in self.get_neighbors(current_zone):
                # Don't visit blocked zones!
                if neighbor.zone_type.value == "blocked":
                    continue

                if neighbor.name not in visited:
                    visited.add(neighbor.name)
                    # Create a new path by adding the neighbor, and put it in the queue
                    new_path = list(current_path)
                    new_path.append(neighbor)
                    queue.append(new_path)

        # If the queue empties and we never found the end, there is no path
        return None
