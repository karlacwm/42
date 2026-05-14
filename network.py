from typing import Optional, Any
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
    colour: str = "grey"
    max_drones: int = 1
    current_drones: list[Any] = field(default_factory=list)

    @property
    def is_full(self) -> bool:
        """Dynamically checks if the zone is full."""
        return len(self.current_drones) >= self.max_drones


@dataclass
class Connection:
    """Represents the connection path between two zones."""
    zone1: Zone
    zone2: Zone
    max_link_capacity: int = 1


def connection_pair(z1: Zone, z2: Zone) -> tuple[str, str]:
    if z1.name <= z2.name:
        return z1.name, z2.name
    return z2.name, z1.name


class Network:
    """The main network holding all zones and connections."""

    def __init__(self) -> None:
        self.zones: dict[str, Zone] = {}
        self.connections: list[Connection] = []
        self.start_hub: Optional[Zone] = None
        self.end_hub: Optional[Zone] = None

    def add_zone(self, zone: Zone) -> None:
        self.zones[zone.name] = zone

    def add_connection(self, conn: Connection) -> None:
        self.connections.append(conn)
