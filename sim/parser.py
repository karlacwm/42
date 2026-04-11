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
    ZONE_NAME_PATTERN = re.compile(r"^[^\s-]+$")

    def __init__(self, filepath: str) -> None:
        self.filepath: str = filepath
        self.network: Network = Network()
        self.drones_total = 0
        self._connection_keys: set[frozenset[str]] = set()
        self._seen_nb_drones = False

    def _error(self, row: int, cause: str) -> ParseError:
        return ParseError(f"Parsing error on line {row}: {cause}")

    def _parse_positive_int(self, raw_value: str, row: int, field: str) -> int:
        try:
            value = int(raw_value)
        except ValueError as exc:
            raise self._error(
                row,
                f"{field} must be an integer, got '{raw_value}'",
            ) from exc
        if value <= 0:
            raise self._error(
                row,
                f"{field} must be a positive integer, got {value}",
            )
        return value

    def _split_base_and_metadata(
        self,
        line: str,
        row: int,
    ) -> tuple[str, dict[str, str]]:
        metadata: dict[str, str] = {}
        has_bracket = "[" in line or "]" in line

        if not has_bracket:
            return line.strip(), metadata

        metadata_match = re.search(r"\[[^\[\]]*\]\s*$", line)
        if not metadata_match:
            raise self._error(row, "invalid metadata block syntax")

        base = line[:metadata_match.start()].rstrip()
        if "[" in base or "]" in base:
            raise self._error(row, "invalid metadata block syntax")

        block = metadata_match.group()[1:-1].strip()
        if block:
            for token in block.split():
                if token.count("=") != 1:
                    raise self._error(row, f"invalid metadata entry '{token}'")
                key, value = token.split("=", 1)
                if not key or not value:
                    raise self._error(row, f"invalid metadata entry '{token}'")
                if key in metadata:
                    raise self._error(row, f"duplicate metadata key '{key}'")
                metadata[key] = value

        return base.strip(), metadata

    def _parse_zone_line(
        self,
        key: str,
        base_line: str,
        metadata: dict[str, str],
        row: int,
    ) -> None:
        elements = base_line.split()
        if len(elements) != 4:
            raise self._error(
                row,
                "zone line must be: "
                "<hub_type> <name> <x> <y> [metadata]",
            )

        zone_name = elements[1]
        if not self.ZONE_NAME_PATTERN.match(zone_name):
            raise self._error(
                row,
                f"invalid zone name '{zone_name}' "
                "(dashes/spaces are not allowed)",
            )
        if zone_name in self.network.zones:
            raise self._error(row, f"duplicate zone name '{zone_name}'")

        try:
            x = int(elements[2])
        except ValueError as exc:
            raise self._error(
                row,
                f"x coordinate must be an integer, got '{elements[2]}'",
            ) from exc

        try:
            y = int(elements[3])
        except ValueError as exc:
            raise self._error(
                row,
                f"y coordinate must be an integer, got '{elements[3]}'",
            ) from exc

        zone_type_raw = metadata.get("zone", "normal")
        if zone_type_raw not in {z.value for z in ZoneType}:
            valid_types = ", ".join(z.value for z in ZoneType)
            raise self._error(
                row,
                f"invalid zone type '{zone_type_raw}' "
                f"(valid: {valid_types})",
            )

        max_drones = self._parse_positive_int(
            metadata.get("max_drones", "1"),
            row,
            "max_drones",
        )
        colour = metadata.get("color", "grey")

        zone = Zone(
            name=zone_name,
            x=x,
            y=y,
            zone_type=ZoneType(zone_type_raw),
            colour=colour,
            max_drones=max_drones,
        )
        self.network.add_zone(zone)

        if key == "start_hub:":
            if self.network.start_hub is not None:
                raise self._error(
                    row,
                    "multiple start_hub definitions are not allowed",
                )
            self.network.start_hub = zone
        elif key == "end_hub:":
            if self.network.end_hub is not None:
                raise self._error(
                    row,
                    "multiple end_hub definitions are not allowed",
                )
            self.network.end_hub = zone

    def _parse_connection_line(
        self,
        base_line: str,
        metadata: dict[str, str],
        row: int,
    ) -> None:
        elements = base_line.split()
        if len(elements) != 2:
            raise self._error(
                row,
                "connection line must be: "
                "connection: <zone1>-<zone2> [metadata]",
            )

        link_token = elements[1]
        if link_token.count("-") != 1:
            raise self._error(
                row,
                "connection must use format <zone1>-<zone2>",
            )

        zone1_name, zone2_name = link_token.split("-", 1)
        if not zone1_name or not zone2_name:
            raise self._error(row, "connection must include two zone names")

        if (
            zone1_name not in self.network.zones
            or zone2_name not in self.network.zones
        ):
            raise self._error(
                row,
                "connections must reference only previously defined zones",
            )
        if zone1_name == zone2_name:
            raise self._error(row, "self-connections are not allowed")

        connection_key = frozenset((zone1_name, zone2_name))
        if connection_key in self._connection_keys:
            raise self._error(
                row,
                f"duplicate connection '{zone1_name}-{zone2_name}'",
            )

        max_link_capacity = self._parse_positive_int(
            metadata.get("max_link_capacity", "1"),
            row,
            "max_link_capacity",
        )

        connection = Connection(
            zone1=self.network.zones[zone1_name],
            zone2=self.network.zones[zone2_name],
            max_link_capacity=max_link_capacity,
        )
        self.network.add_connection(connection)
        self._connection_keys.add(connection_key)

    def parse(self) -> None:
        try:
            with open(self.filepath) as maps:
                lines = maps.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"Map file not found: {self.filepath}")

        first_content_seen = False

        for row, line in enumerate(lines, start=1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            base_line, metadata = self._split_base_and_metadata(line, row)
            if not base_line:
                raise self._error(
                    row,
                    "line contains metadata but no directive",
                )

            key = base_line.split()[0]

            if not first_content_seen:
                first_content_seen = True
                if key != "nb_drones:":
                    raise self._error(
                        row,
                        "the first map directive must be "
                        "'nb_drones: <positive_integer>'",
                    )

            if key == "nb_drones:":
                if self._seen_nb_drones:
                    raise self._error(
                        row,
                        "nb_drones can only be defined once",
                    )
                if metadata:
                    raise self._error(
                        row,
                        "nb_drones does not accept metadata",
                    )

                elements = base_line.split()
                if len(elements) != 2:
                    raise self._error(
                        row,
                        "nb_drones line must be: "
                        "nb_drones: <positive_integer>",
                    )

                self.drones_total = self._parse_positive_int(
                    elements[1],
                    row,
                    "nb_drones",
                )
                self._seen_nb_drones = True

            elif key in {"hub:", "start_hub:", "end_hub:"}:
                self._parse_zone_line(key, base_line, metadata, row)

            elif key == "connection:":
                self._parse_connection_line(base_line, metadata, row)

            else:
                raise self._error(row, f"unknown directive '{key}'")

        eof_line = len(lines) + 1
        if not self._seen_nb_drones:
            raise self._error(
                eof_line,
                "missing required 'nb_drones: <positive_integer>'",
            )
        if self.network.start_hub is None:
            raise self._error(
                eof_line,
                "missing required start_hub definition",
            )
        if self.network.end_hub is None:
            raise self._error(eof_line, "missing required end_hub definition")
