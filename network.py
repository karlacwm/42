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
    colour: str = "grey"
    max_drones: int = 1
    current_drones: List['Drone'] = field(default_factory=list)

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


class Network:
    """The main network holding all zones and connections."""

    def __init__(self) -> None:
        self.zones: dict[str, Zone] = {}
        self.connections: List[Connection] = []
        self.start_hub: Optional[Zone] = None
        self.end_hub: Optional[Zone] = None

    def add_zone(self, zone: Zone) -> None:
        self.zones[zone.name] = zone

    def add_connection(self, connection: Connection) -> None:
        self.connections.append(connection)

    def __repr__(self) -> str:
        return (
            "network parsed:\n\n"
            f"zones:\n{self.zones}\n\n"
            f"start:\n{self.start_hub}\n\n"
            f"end:\n{self.end_hub}\n\n"
            f"connections:\n{self.connections}")


@dataclass
class Drone:
    """Represents one drone unit"""
    _id: str
    x: int
    y: int
    reached_goal: bool = field(init=False)
    next_zone: Optional[Zone]
    cooldown: int = 0
    shotdown: bool = False

    def cooling_down(self) -> None:
        """Updates the cooldown status in restricted zones."""
        if self.cooldown > 0:
            self.cooldown -= 1
        else:
            pass
