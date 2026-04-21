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
        self.unique_names: list[str] = []

    def lookup_config(self, line: str, row: int) -> dict[str, str] | None:
        config = re.search(r"\[(\S*\s?)*\]", line)
        if not config:
            return None
        try:
            config_str = config.group().strip("[]")
            return {pair.split("=")[0]: pair.split("=")[1]
                    for pair in config_str.split()}
        except IndexError:
            raise ParseError(
                f"Parsing error: Invalid map config on line {row}\n"
                "Invalid metadata block format :(\n"
                "It must be e.g. [zone=... color=... max_drones=...] for zones"
                ", or [max_link_capacity=...] for connections")

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
                self.drones_total = int(elements[1]) if int(
                    elements[1]) > 0 else 0
                if not self.drones_total > 0:
                    raise ParseError(
                        f"Parsing error: Invalid map config on line {row}\n"
                        "Number of drones must be a positive integer :(")

            elif key in ["hub:", "start_hub:", "end_hub:"]:
                config = self.lookup_config(line, row) or {}

                if config.get("zone"):
                    config_type = config.get("zone")
                    try:
                        ZoneType(config_type)
                    except ValueError:
                        raise ParseError(
                            f"Parsing error: Invalid map config on line {row}"
                            "\nZone type must be one of normal, blocked, "
                            "restricted or priority :("
                        )
                else:
                    config_type = config.get("zone", "normal")

                config_colour = config.get("color", "grey")

                config_max_drones = int(config.get("max_drones", 1))
                if not config_max_drones > 0:
                    raise ParseError(
                        f"Parsing error: Invalid map config on line {row}\n"
                        "Max number of drones must be a positive integer :(")

                try:
                    int(elements[2])
                    int(elements[3])
                except ValueError:
                    raise ParseError(
                        f"Parsing error: Invalid map config on line {row}\n"
                        "Coordinates must be integers :(")

                if " " and "-" not in elements[1]:
                    if elements[1] not in self.unique_names:
                        zone = Zone(
                            name=elements[1],
                            x=int(elements[2]),
                            y=int(elements[3]),
                            zone_type=ZoneType(config_type),
                            colour=config_colour,
                            max_drones=config_max_drones)
                        self.unique_names.append(elements[1])
                        self.network.add_zone(zone)
                    else:
                        raise ParseError(
                            f"Parsing error: Invalid map config on line {row}"
                            "\nZone name is repeated :(")
                else:
                    raise ParseError(
                        f"Parsing error: Invalid map config on line {row}\n"
                        "Invalid characters in zone name, no dashes or "
                        "spaces allowed :("
                    )

                if key == "start_hub:":
                    if not self.network.start_hub:
                        self.network.start_hub = zone
                    else:
                        raise ParseError(
                            f"Parsing Error: Invalid map config on line {row}"
                            "\nOnly one start_hub is allowed :(")
                elif key == "end_hub:":
                    if not self.network.end_hub:
                        self.network.end_hub = zone
                    else:
                        raise ParseError(
                            f"Parsing Error: Invalid map config on line {row}"
                            "\nOnly one end_hub is allowed :(")

            elif key == "connection:":
                config = self.lookup_config(line, row) or {}

                config_link_cap = int(config.get("max_link_capacity", 1))
                if not config_link_cap > 0:
                    raise ParseError(
                        f"Parsing error: Invalid map config on line {row}\n"
                        "Max link capacity must be a positive integer :(")

                zone1_key = elements[1].split("-")[0]
                zone2_key = elements[1].split("-")[1]

                try:
                    zone1 = self.network.zones[zone1_key]
                    zone2 = self.network.zones[zone2_key]
                except KeyError:
                    raise ParseError(
                        f"Parsing Error: Invalid map config on line {row}\n"
                        "Zone(s) in the connection not yet defined before :(")

                connection = Connection(
                    zone1=zone1,
                    zone2=zone2,
                    max_link_capacity=config_link_cap
                )
                same_connection = Connection(
                    zone1=connection.zone2,
                    zone2=connection.zone1,
                    max_link_capacity=config_link_cap
                )
                if (connection not in self.network.connections and
                        same_connection not in self.network.connections):
                    self.network.add_connection(connection)
                else:
                    raise ParseError(
                        f"Parsing error: Invalid map config on line {row}\n"
                        "Connection already exist. No duplicates allowed :("
                    )

        if not self.network.start_hub:
            raise ParseError("Parsing error: The start_hub is missing :(")
        elif not self.network.end_hub:
            raise ParseError("Parsing error: The end_hub is missing :(")
