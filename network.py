"""Defines the core structures for the drone network graph."""
from typing import List, Optional
from enum import Enum
from dataclasses import dataclass, field


class ZoneType(str, Enum):
    """Defines a set of valid types of zones."""
    normal = "normal"
    blocked = "blocked"
    restricted = "restricted"
    priority = "priority"


@dataclass
class Zone:
    """Represents a zone in the drone network."""
    name: str
    x: int
    y: int
    zone_type: ZoneType = ZoneType.normal
    colour: Optional[str] = None
    max_drones: int = 1
    current_drones: List['Drone'] = field(default_factory=list)
    is_full: bool = field(init=False)
# self.is_full = len(self.current_drones) > self.max_drones


@dataclass
class Connection:
    """Represents the connection path between two zones."""
    zone1: Zone
    zone2: Zone
    max_link_capacity: int = 1


class Network:
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


class Drone:
    """Represents one drone unit"""
