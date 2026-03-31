"""
Class MapParser reads a map file and creates a Graph object,
validating the format and content of the file.
It raises ParseError for any issues.
"""
import re
from typing import Tuple, Dict
from network import Zone, Connection, Graph


class ParseError(Exception):
    """Custom exception for parsing errors with line numbers."""
    pass


class MapParser:
    def __init__(self, filepath: str) -> None:
        self.filepath: str = filepath
        self.graph: Graph = Graph()
        self.nb_drones: int = 0
        self.start_count: int = 0
        self.end_count: int = 0

    def parse_metadata(self, line: str) -> Dict[str, str]:
        """Extracts metadata from brackets, e.g., [zone=priority color=red]."""
        metadata = {}
        match = re.search(r'\[(.*?)\]', line)
        if match:
            tags = match.group(1).split()
            for tag in tags:
                if '=' in tag:
                    key, value = tag.split('=', 1)
                    metadata[key] = value
        return metadata

    def parse(self) -> Tuple[Graph, int]:
        with open(self.filepath, 'r') as file:
            for line_num, line in enumerate(file, 1):
                # Ignore comments and empty lines
                clean_line = line.split('#')[0].strip()
                if not clean_line:
                    continue

                try:
                    self._process_line(clean_line)
                except Exception as e:
                    # Catch any error and append the line number as required
                    raise ParseError(f"Error on line {line_num}: {str(e)}")

        # Final validation
        if self.start_count != 1 or self.end_count != 1:
            raise ParseError(
                "Map must have exactly one start_hub and one end_hub.")
        if self.nb_drones <= 0:
            raise ParseError("Number of drones must be a positive integer.")

        return self.graph, self.nb_drones

    def _process_line(self, line: str) -> None:
        metadata = self.parse_metadata(line)

        # Remove metadata part from line for easier base parsing
        base_line = re.sub(r'\[.*?\]', '', line).strip()
        parts = base_line.split()

        if not parts:
            return

        prefix = parts[0]

        if prefix == "nb_drones:":
            self.nb_drones = int(parts[1])
            if self.nb_drones <= 0:
                raise ValueError("nb_drones must be positive.")

        elif prefix in ("hub:", "start_hub:", "end_hub:"):
            if len(parts) < 4:
                raise ValueError(
                    "Zone definition must include name, x, and y.")

            name = parts[1]
            if '-' in name:
                raise ValueError("Zone names cannot contain dashes.")

            x, y = int(parts[2]), int(parts[3])

            # Extract metadata with defaults
            zone_type = metadata.get("zone", "normal")
            color = metadata.get("color", None)
            max_drones = int(metadata.get("max_drones", 1))

            if zone_type not in ["normal", "blocked",
                                 "restricted", "priority"]:
                raise ValueError(f"Invalid zone type: {zone_type}")

            zone = Zone(name, x, y, zone_type, color, max_drones)

            if name in self.graph.zones:
                raise ValueError(f"Duplicate zone name: {name}")

            self.graph.add_zone(zone)

            if prefix == "start_hub:":
                self.graph.start_hub = zone
                self.start_count += 1
            elif prefix == "end_hub:":
                self.graph.end_hub = zone
                self.end_count += 1

        elif prefix == "connection:":
            if len(parts) < 2:
                raise ValueError("Connection must specify zones.")

            link = parts[1]
            if link.count('-') != 1:
                raise ValueError("Connection must be in format zone1-zone2.")

            z1_name, z2_name = link.split('-')
            if z1_name not in self.graph.zones or (
                    z2_name not in self.graph.zones):
                raise ValueError("Connection references unknown zone.")

            z1, z2 = self.graph.zones[z1_name], self.graph.zones[z2_name]
            max_cap = int(metadata.get("max_link_capacity", 1))

            # Check for duplicates
            for existing in self.graph.connections:
                if (existing.zone1 == z1 and existing.zone2 == z2) or \
                   (existing.zone1 == z2 and existing.zone2 == z1):
                    raise ValueError("Duplicate connection found.")

            conn = Connection(z1, z2, max_link_capacity=max_cap)
            self.graph.add_connection(conn)

        else:
            raise ValueError(f"Unknown line prefix: {prefix}")
