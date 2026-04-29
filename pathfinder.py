from network import Network, Zone, ZoneType
from typing import Optional


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

    def find_efficient_path(self, path_options: list[list[Zone]]
                            ) -> tuple[list[Zone], float]:
        cost_pair: list[tuple[list[Zone], float]] = []
        for path in path_options:
            cost: float = 0
            for zone in path:
                if zone.zone_type == ZoneType.normal:
                    cost += 1
                elif zone.zone_type == ZoneType.priority:
                    cost += 0.5
                elif zone.zone_type == ZoneType.restricted:
                    cost += 5
            cost_pair.append((path, cost))
        cost_pair = sorted(
            cost_pair, key=lambda lowest: lowest[1], reverse=False)
        return cost_pair[0]

    def find_path(self) -> Optional[list[Zone]]:
        start = self.network.start_hub
        end = self.network.end_hub
        if not start or not end:
            return None

        visited = [start.name]
        path = [[start]]

        while path:
            current_path = path.pop(0)
            current_zone = current_path[-1]

            if current_zone == end:
                best_path = self.find_efficient_path(path)
                return best_path[0]

            ways = self.find_neighbour(current_zone)
            for neighbour in ways:
                if neighbour.name not in visited and \
                        neighbour.zone_type is not ZoneType.blocked:
                    visited.append(neighbour.name)
                    new_path = list(current_path)
                    new_path.append(neighbour)
                    path.append(new_path)
        return None


# cost
# zone type
# zone max
# conn max
