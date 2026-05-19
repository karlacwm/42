"""Network primitives: Zone, Connection and Network container."""

from typing import Optional, Any
from enum import Enum
from dataclasses import dataclass, field


class ZoneType(str, Enum):
    """Enumeration of allowed zone types."""
    normal = "normal"
    blocked = "blocked"
    restricted = "restricted"
    priority = "priority"


@dataclass
class Zone:
    """A node in the network representing a physical zone."""
    name: str
    x: int
    y: int
    zone_type: ZoneType = ZoneType.normal
    colour: str = "grey"
    max_drones: int = 1
    current_drones: list[Any] = field(default_factory=list)

    @property
    def is_full(self) -> bool:
        """Return True when number of drones meets capacity."""
        return len(self.current_drones) >= self.max_drones


@dataclass
class Connection:
    """An undirected link between two `Zone` objects."""
    zone1: Zone
    zone2: Zone
    max_link_capacity: int = 1


def connection_pair(z1: Zone, z2: Zone) -> tuple[str, str]:
    """Return a canonical ordered pair of zone names for dict keys."""

    if z1.name <= z2.name:
        return z1.name, z2.name
    return z2.name, z1.name


class Network:
    """Container holding zones, connections and start/end hubs."""

    def __init__(self) -> None:
        """Create an empty `Network` object."""

        self.zones: dict[str, Zone] = {}
        self.connections: list[Connection] = []
        self.start_hub: Optional[Zone] = None
        self.end_hub: Optional[Zone] = None

    def add_zone(self, zone: Zone) -> None:
        """Register a `Zone` in the network by its name."""

        self.zones[zone.name] = zone

    def add_connection(self, conn: Connection) -> None:
        """Add a `Connection` object to the network's connections."""

        self.connections.append(conn)
