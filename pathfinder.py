from network import Network, Zone, ZoneType
from typing import Optional
import heapq


class Pathfinder:
    def __init__(self, network: Network) -> None:
        self.network = network

    def find_neighbour(self, current_zone: Zone | None) -> list[Zone]:
        neighbour_list = []

        for conn in self.network.connections:
            if current_zone == conn.zone1:
                neighbour_list.append(conn.zone2)
            elif current_zone == conn.zone2:
                neighbour_list.append(conn.zone1)
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

    def find_path(self) -> Optional[list[Zone]]:
        start = self.network.start_hub
        end = self.network.end_hub
        cost = 0.0
        if not start or not end:
            return None

        visited = {start.name: cost}
        path = [(cost, [start])]
        heapq.heapify(path)

        while path:
            current_cost, current_path = heapq.heappop(path)
            current_zone = current_path[-1]

            if current_zone == end:
                return current_path

            ways = self.find_neighbour(current_zone)
            for neighbour in ways:
                if neighbour.zone_type is not ZoneType.blocked:
                    visit_cost = current_cost + self.get_cost(neighbour)
                    if visit_cost < visited[neighbour.name]:
                        visited[neighbour.name] = visit_cost

                    new_path = list(current_path)
                    new_path.append(neighbour)
                    heapq.heappush(path, (visit_cost, new_path))
        print(path)
        return None


# cost
# zone type
# zone max
# conn max
