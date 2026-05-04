from network import Network, Zone, ZoneType, Connection, connection_pair
from typing import Optional
from itertools import count
import heapq


TrafficMap = dict[tuple[str, str], int]


class Pathfinder:
    def __init__(self, network: Network) -> None:
        self.network = network

    def find_neighbour(
            self, current_zone: Zone | None) -> list[tuple[Zone, Connection]]:
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
        if zone.zone_type == ZoneType.priority:
            return 0.5
        elif zone.zone_type == ZoneType.restricted:
            return 5
        else:
            return 1

    def get_connection_cost(
            self, conn: Connection, traffic: TrafficMap) -> float:
        key = connection_pair(conn.zone1, conn.zone2)
        usage = traffic.get(key, 0)

        if usage <= conn.max_link_capacity:
            return usage / conn.max_link_capacity

        overflow = usage - conn.max_link_capacity + 1
        return (usage / conn.max_link_capacity) + (overflow * 5)

    def find_path(self, traffic: TrafficMap) -> Optional[list[Zone]]:
        start = self.network.start_hub
        end = self.network.end_hub
        cost = 0.0
        if not start or not end:
            return None

        step = count()
        visited = {start.name: cost}
        path = [(cost, next(step), [start])]
        heapq.heapify(path)

        while path:
            current_cost, _, current_path = heapq.heappop(path)
            current_zone = current_path[-1]

            if current_zone == end:
                return current_path

            ways = self.find_neighbour(current_zone)
            for neighbour, conn in ways:
                if neighbour.zone_type == ZoneType.blocked:
                    continue

                visit_cost = (
                    current_cost
                    + self.get_cost(neighbour)
                    + self.get_connection_cost(conn, traffic)
                )

                prev_cost = visited.get(neighbour.name)
                if prev_cost is None or visit_cost < prev_cost:
                    visited[neighbour.name] = visit_cost

                    new_path = list(current_path)
                    new_path.append(neighbour)
                    heapq.heappush(path, (visit_cost, next(step), new_path))
        return None

# note to self
# dijkstra + maximum flow
# o | cost
# o | zone type
# x | zone max (put in sim?)
# x | conn max (sim)
