"""
Class MapParser reads a map file and creates a Network object,
validating the format and content of the map file.
It raises ParseError for any parsing-related issues.
"""
import re


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
            print(row, line)
            match = re.match(r'^([a-z]*_?[a-z]*:)\s*([0-9]*\s*)$', line)
            print(match)

        


# test python3 parser.py
parser = MapParser("/home/wcheung/git-fly/maps/easy/01_linear_path.txt")
parser.parse()
