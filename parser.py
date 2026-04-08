"""
Class MapParser reads a map file and creates a Network object,
validating the format and content of the map file.
It raises ParseError for any parsing-related issues.
"""
from network import Zone, Connection


class ParseError(Exception):
    """Custom exception for parsing-related errors."""
    pass


class MapParser:
    def __init__(self, filepath: str) -> None:
        self.filepath: str = filepath

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
            # print(row, line)
            
            elements = line.split()
            key = elements[0]
            if key == "nb_drones:":
                drones_total = elements[1]
                # print(drones_total)

            elif key in ["hub:", "start_hub:", "end_hub:"]:
                zone = Zone(elements[1], elements[2], elements[3])
                # print(zone)
                
            elif key == "connection:":
                zone1 = elements[1].split("-")[0]
                zone2 = elements[1].split("-")[1]
                connection = Connection(zone1, zone2)
                # print(connection)
            else:
                raise ParseError(f"Parsing error: Invalid map config on line {row}")

        


# test python3 parser.py
parser = MapParser("/workspaces/fly-in/maps/easy/01_linear_path.txt")
parser.parse()
