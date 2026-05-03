from network import Network, Zone, ZoneType, Connection
from typing import Optional
from itertools import count
import heapq


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

    def path_is_full(self, conn: Connection, traffic: dict) -> bool:
        status = traffic.get(conn, 0)

        if status >= conn.max_link_capacity:
            return True
        return False

    def find_path(self) -> Optional[list[Zone]]:
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
                print(current_path)
                return current_path

            ways = self.find_neighbour(current_zone)
            for neighbour, conn in ways:
                if neighbour.zone_type is not ZoneType.blocked and \
                        not self.path_is_full(conn, traffic):
                    visit_cost = current_cost + self.get_cost(neighbour)
                    prev_cost = visited.get(neighbour.name)
                    if prev_cost is None or visit_cost < prev_cost:
                        visited[neighbour.name] = visit_cost

                        new_path = list(current_path)
                        new_path.append(neighbour)
                        heapq.heappush(
                            path, (visit_cost, next(step), new_path))
        return None

# note to self
# dijkstra + maximum flow
# o | cost
# o | zone type
# x | zone max (put in sim?)
# x | conn max (sim)
