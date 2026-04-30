import heapq
from network import Network, Zone, ZoneType
from typing import Optional
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

    while queue:
        # Pop the CHEAPEST path we are currently exploring
        current_cost, current_path = heapq.heappop(queue)
        current_zone = current_path[-1]

        # Because heapq always gives us the cheapest path, the FIRST
        # time we hit the end hub, it is mathematically guaranteed to be the best path!
        if current_zone == end:
            return current_path

        ways = self.find_neighbour(current_zone)
        for neighbour in ways:
            if neighbour.zone_type == ZoneType.blocked:
                continue

            # Calculate what it would cost to step here
            new_cost = current_cost + self.get_cost(neighbour)

            # Have we never been here? Or did we find a CHEAPER way to get here?
            if neighbour.name not in visited_costs or new_cost < visited_costs[neighbour.name]:
                # Update our records
                visited_costs[neighbour.name] = new_cost

                # Add it to the queue to explore later
                new_path = list(current_path)
                new_path.append(neighbour)
                heapq.heappush(queue, (new_cost, new_path))

    return None
