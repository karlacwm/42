"""Defines the core structures for the drone network graph."""
from typing import List, Optional


class Zone:
    """Represents a zone (or hub) in the drone network."""

    def __init__(self, name: str, x: int, y: int, zone_type: str = "normal",
                 color: Optional[str] = None, max_drones: int = 1) -> None:
        self.name: str = name
        self.x: int = x
        self.y: int = y
        self.zone_type: str = zone_type
        self.color: Optional[str] = color
        self.max_drones: int = max_drones
        self.current_drones: int = 0


class Connection:
    """Represents the connection path between two zones."""

    def __init__(self, zone1: Zone, zone2: Zone,
                 max_link_capacity: int = 1) -> None:
        self.zone1: Zone = zone1
        self.zone2: Zone = zone2
        self.max_link_capacity: int = max_link_capacity


class Graph:
    """The main network holding all zones and connections."""

    def __init__(self) -> None:
        self.zones: dict[str, Zone] = {}
        self.connections: List[Connection] = []
        self.start_hub: Optional[Zone] = None
        self.end_hub: Optional[Zone] = None

    def add_zone(self, zone: Zone) -> None:
        self.zones[zone.name] = zone

    def add_connection(self, conn: Connection) -> None:
        self.connections.append(conn)
