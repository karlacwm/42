"""
Class MapParser reads a map file and creates a Network object,
validating the format and content of the map file.
It raises ParseError for any parsing-related issues.
"""
# use pydantic??


class ParseError(Exception):
    """Custom exception for parsing-related errors."""
    pass


class MapParser:
    def __init__(self, filepath: str) -> None:
        self.filepath: str = filepath
