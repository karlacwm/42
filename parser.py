"""Parse map files and build a Network."""
import re
from network import Zone, Connection, Network, ZoneType


class ParseError(Exception):
    """Custom exception for parsing-related errors."""
    pass


class MapParser:
    """Parse a map file into a Network and store parser state."""

    def __init__(self, filepath: str) -> None:
        self.filepath: str = filepath
        self.network: Network = Network()
        self.drones_total = 0
        self.unique_names: list[str] = []

    def lookup_config(self, line: str, row: int) -> dict[str, str] | None:
        """Extract a metadata config dict from a map line or return None."""

        config = re.search(r"\[(\S*\s?)*\]", line)
        if not config:
            return None
        group = config.group()
        if group.count('[') != 1 or group.count(']') != 1:
            raise ParseError(
                f"Parsing error: Invalid map config on line {row}\n"
                "Must have only a single '[' and ']' for the metablock :(")

        config_str = group.strip("[]").strip()
        if not config_str:
            raise ParseError(
                f"Parsing error: Invalid map config on line {row}\n"
                "Empty metadata block: expected something like"
                " [zone=... color=...]")

        parts = config_str.split()
        config_dict: dict[str, str] = {}
        for pair in parts:
            if pair.count('=') != 1:
                raise ParseError(
                    f"Parsing error: Invalid map config on line {row}\n"
                    f"Each metadata pair must contain exactly one '='")
            key, value = pair.split('=', 1)
            key = key.strip()
            value = value.strip()
            if not key or value == "":
                raise ParseError(
                    f"Parsing error: Invalid map config on line {row}\n"
                    f"Key and value must not be empty :(")
            if key not in ["zone", "color", "max_drones",
                           "max_link_capacity"]:
                raise ParseError(
                    f"Parsing error: Invalid map config on line {row}\n"
                    f"Unknown metadata key '{key}'")
            config_dict[key] = value

        return config_dict

    def parse(self) -> None:
        """Parse the map file and populate the `network` attribute."""
        try:
            with open(self.filepath) as maps:
                lines = maps.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"Map file not found: {self.filepath}")

        for row, line in enumerate(lines, start=1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if '#' in line:
                line = line.split('#', 1)[0].rstrip()
                if not line:
                    continue

            elements = line.split()
            key = elements[0]
            if key not in ["nb_drones:", "connection:",
                           "hub:", "start_hub:", "end_hub:"]:
                raise ParseError(
                    f"Parsing error: Unknown map config on line {row}\nCheck"
                    " if there is any missing space, missing element "
                    "or invalid zone type :(")
            elif key == "nb_drones:":
                if len(elements) == 2:
                    try:
                        self.drones_total = int(elements[1]) if int(
                            elements[1]) > 0 else 0
                    except ValueError:
                        raise ParseError(
                            f"Parsing error: Invalid map config on line {row}"
                            "\nNumber of drones must be a positive integer :(")
                else:
                    raise ParseError(
                        "Parsing error: The config with the number of "
                        "drones is invalid :(")
                if self.drones_total <= 0:
                    raise ParseError(
                        f"Parsing error: Invalid map config on line {row}"
                        "\nNumber of drones must be a positive integer :(")

            elif key in ["hub:", "start_hub:", "end_hub:"]:
                if len(elements) > 4 and "[" in line and "]" in line:
                    config = self.lookup_config(line, row) or {}
                elif len(elements) == 4:
                    config = {}
                else:
                    raise ParseError(
                        f"Parsing error: Invalid map config on line {row}"
                        "\nThe brackets \"[]\" are missing or not properly "
                        "opened or closed :(")

                if config.get("zone"):
                    config_type = config.get("zone")
                    try:
                        ZoneType(config_type)
                    except ValueError:
                        raise ParseError(
                            "Parsing error: Invalid map config on line"
                            f" {row}\nZone type must be one of normal,"
                            " blocked, restricted or priority :(")
                else:
                    config_type = config.get("zone", "normal")

                config_colour = config.get("color", "grey")

                try:
                    config_max_drones = int(config.get("max_drones", 1))
                except ValueError:
                    raise ParseError(
                        "Parsing error: Invalid map config on line"
                        f" {row}\nMax number of drones must be a positive"
                        " integer :(")
                if not config_max_drones > 0:
                    raise ParseError(
                        "Parsing error: Invalid map config on line"
                        f" {row}\nMax number of drones must be a positive"
                        " integer :(")

                try:
                    int(elements[2])
                    int(elements[3])
                except ValueError:
                    raise ParseError(
                        f"Parsing error: Invalid map config on line {row}"
                        "\nZone name must not have spaces and coordinates "
                        "must be integers :(")

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
                            "Parsing error: Invalid map config on line"
                            f" {row}\nZone name is repeated :(")
                else:
                    raise ParseError(
                        "Parsing error: Invalid map config on line"
                        f" {row}\nInvalid characters in zone name, "
                        "no dashes or spaces allowed :("
                    )

                if key == "start_hub:":
                    if not self.network.start_hub:
                        self.network.start_hub = zone
                    else:
                        raise ParseError(
                            "Parsing Error: Invalid map config on line"
                            f" {row}\nOnly one start_hub is allowed :(")
                elif key == "end_hub:":
                    if not self.network.end_hub:
                        self.network.end_hub = zone
                    else:
                        raise ParseError(
                            "Parsing Error: Invalid map config on line"
                            f" {row}\nOnly one end_hub is allowed :(")

            elif key == "connection:":
                if len(elements) > 2 and "[" in line and "]" in line:
                    config = self.lookup_config(line, row) or {}
                elif len(elements) == 2:
                    config = {}
                else:
                    raise ParseError(
                        f"Parsing error: Invalid map config on line {row}"
                        "\nThe brackets \"[]\" are missing or not properly "
                        "opened or closed :(")

                try:
                    config_link_cap = int(config.get("max_link_capacity", 1))
                except ValueError:
                    raise ParseError(
                        "Parsing error: Invalid map config on line"
                        f" {row}\nMax link capacity must be a positive"
                        " integer :(")
                if not config_link_cap > 0:
                    raise ParseError(
                        "Parsing error: Invalid map config on line"
                        f" {row}\nMax link capacity must be a positive"
                        " integer :(")

                zone1_key = elements[1].split("-")[0]
                zone2_key = elements[1].split("-")[1]

                try:
                    zone1 = self.network.zones[zone1_key]
                    zone2 = self.network.zones[zone2_key]
                except KeyError:
                    raise ParseError(
                        "Parsing Error: Invalid map config on line"
                        f" {row}\nZone(s) in the connection not yet"
                        " defined before :(")

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
                        "Parsing error: Invalid map config on line"
                        f" {row}\nConnection already exist. No duplicates"
                        " allowed :("
                    )

        if not self.network.start_hub:
            raise ParseError("Parsing error: The start_hub is missing :(")
        elif not self.network.end_hub:
            raise ParseError("Parsing error: The end_hub is missing :(")
