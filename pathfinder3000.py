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

    def find_shortest_path(self, start: Zone,
                           end: Zone) -> Optional[List[Zone]]:
        queue = [[start]]
        visited = {start.name}

        while queue:
            current_path = queue.pop(0)
            current_zone = current_path[-1]

            if current_zone.name == end.name:
                return current_path

            for neighbor in self.get_neighbors(current_zone):
                if (neighbor.zone_type.value != "blocked" and
                        neighbor.name not in visited):
                    visited.add(neighbor.name)
                    queue.append(current_path + [neighbor])

        return None
