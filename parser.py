"""
Class MapParser reads a map file and creates a Network object,
validating the format and content of the map file.
It raises ParseError for any parsing-related issues.
"""
import re
from network import Zone, Connection, Network, ZoneType


class ParseError(Exception):
    """Custom exception for parsing-related errors."""
    pass


class MapParser:
    def __init__(self, filepath: str) -> None:
        self.filepath: str = filepath
        self.network: Network = Network()
        self.drones_total = 0

    def lookup_config(self, line: str) -> dict[str, str] | None:
        config = re.search(r"\[(\S*\s?)*\]", line)
        if not config:
            return None
        config_str = config.group().strip("[]")
        return {pair.split("=")[0]: pair.split("=")[1]
                for pair in config_str.split()}

    def parse(self) -> None:
        try:
            with open(self.filepath) as maps:
                lines = maps.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"Map file not found: {self.filepath}")

        for row, line in enumerate(lines, start=1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            elements = line.split()
            key = elements[0]
            if key == "nb_drones:":
                self.drones_total = int(elements[1])

            elif key in ["hub:", "start_hub:", "end_hub:"]:
                config = self.lookup_config(line) or {}

                config_type = config.get("zone", "normal")
                config_colour = config.get("color", "grey")
                config_max_drones = int(config.get("max_drones", 1))

                zone = Zone(
                    name=elements[1],
                    x=int(elements[2]),
                    y=int(elements[3]),
                    zone_type=ZoneType(config_type),
                    colour=config_colour,
                    max_drones=config_max_drones)
                self.network.add_zone(zone)

                if key == "start_hub:":
                    self.network.start_hub = zone
                elif key == "end_hub:":
                    self.network.end_hub = zone

            elif key == "connection:":
                config = self.lookup_config(line) or {}

                config_link_cap = int(config.get("max_link_capacity", 1))

                zone1_key = elements[1].split("-")[0]
                zone2_key = elements[1].split("-")[1]

                zone1 = self.network.zones[zone1_key]
                zone2 = self.network.zones[zone2_key]

                connection = Connection(
                    zone1=zone1,
                    zone2=zone2,
                    max_link_capacity=config_link_cap
                )
                self.network.add_connection(connection)

            else:
                raise ParseError(
                    f"Parsing error: Invalid map config on line {row}")
