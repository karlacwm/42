"""Pathfinding utilities that compute least-cost routes in a Network."""

from network import Network, Zone, ZoneType, Connection, connection_pair
from typing import Optional
from itertools import count
import heapq


class Pathfinder:
    """Compute cheapest paths through a Network considering traffic."""

    def __init__(self, network: Network) -> None:
        """Initialize with a Network instance."""
        self.network = network

    def find_neighbour(
            self, current_zone: Zone | None) -> list[tuple[Zone, Connection]]:
        """Return neighbour (Zone, Connection) pairs for current_zone."""

        neighbour_list = []

        for conn in self.network.connections:
            if current_zone == conn.zone1:
                neighbour_list.append((conn.zone2, conn))
            elif current_zone == conn.zone2:
                neighbour_list.append((conn.zone1, conn))
            else:
                continue
        return neighbour_list

    def get_cost(self, zone: Zone) -> float:
        """Return a cost factor for entering zone based on its type."""

        if zone.zone_type == ZoneType.priority:
            return 0.5
        elif zone.zone_type == ZoneType.restricted:
            return 5
        else:
            return 1

    def get_connection_cost(
            self, conn: Connection,
            traffic: dict[tuple[str, str], int]) -> float:
        """Return traversal cost for conn given current traffic."""

        key = connection_pair(conn.zone1, conn.zone2)
        # using tuple as dict key to represent the same connection
        usage = traffic.get(key, 0)

        if usage <= conn.max_link_capacity:
            # 0 is unused, 1 is occupied
            return usage / conn.max_link_capacity

        overflow = usage - conn.max_link_capacity + 1
        # overflow * 5 to make the cost much more expensive
        return (usage / conn.max_link_capacity) + (overflow * 5)

    def find_path(
            self, traffic: dict[tuple[str, str], int]) -> Optional[list[Zone]]:
        """Find the least-cost path from start to end hub or return None."""
        start = self.network.start_hub
        end = self.network.end_hub
        cost = 0.0
        if not start or not end:
            return None

        step = count()
        visited = set()
        path = [(cost, next(step), [start])]
        heapq.heapify(path)

        while path:
            current_cost, _, current_path = heapq.heappop(path)
            current_zone = current_path[-1]

            if current_zone.name in visited:
                continue

            visited.add(current_zone.name)

            if current_zone == end:
                return current_path

            ways = self.find_neighbour(current_zone)
            for neighbour, conn in ways:
                if neighbour.zone_type == ZoneType.blocked:
                    continue

                if neighbour.name in visited:
                    continue

                visit_cost = (
                    current_cost
                    + self.get_cost(neighbour)
                    + self.get_connection_cost(conn, traffic)
                )

                new_path = list(current_path)
                new_path.append(neighbour)
                heapq.heappush(path, (visit_cost, next(step), new_path))
        return None

    def dynamic_pathfinder(self, drones_total: int) -> list[list[Zone]]:
        """Get multiple paths by reserving capacity in temporary traffic."""

        paths: list[list[Zone]] = []
        dynamic_traffic: dict[tuple[str, str], int] = {}
        for _ in range(drones_total):
            path = self.find_path(dynamic_traffic)
            if not path:
                break
            paths.append(path)
            for i in range(len(path) - 1):
                key = connection_pair(path[i], path[i + 1])
                dynamic_traffic[key] = dynamic_traffic.get(key, 0) + 1
        return sorted(paths, key=lambda x: len(x))

# note to self
# dijkstra + maximum flow
# o | cost
# o | zone type
# x | zone max (put in sim?)
# x | conn max (sim)

# pathfinder: given current traffic, what's the cheapest route?
# simulation: can i send a drone on this route? foes it have capacity?
