# python3 -m venv space_venv
# source space_venv/bin/activate
# pip install pydantic

from pydantic import BaseModel, Field, ValidationError
from datetime import datetime


class SpaceStation(BaseModel):
    # without type hints it's just a class variable, not pydantic field
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)

    def print_info(self) -> None:
        print("Valid station created:")
        print(f"ID: {self.station_id}")
        print(f"Name: {self.name}")
        print(f"Crew: {self.crew_size} people")
        print(f"Power: {self.power_level}%")
        print(f"Oxygen: {self.oxygen_level}%")
        # print(f"Last maintenance: {self.last_maintenance}")
        print("Status: "
              f"{'Operational' if self.is_operational else 'Not Operational'}")
        # print(f"Note: {self.notes}")
        print()


def main() -> None:
    print("Space Station Data Validation")
    print("=" * 40)

    try:
        station1 = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime(2026, 3, 16),
            # last_maintenance="2026-03-16T22:30:00Z",
            notes="The first space station ever"
        )
        station1.print_info()

        print("=" * 40)
        print("Expected validation error:")

        station2 = SpaceStation(
            station_id="ISS002",
            name="International Space Station",
            crew_size=22,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.now()
        )
        station2.print_info()

    except ValidationError as e:
        error_message = e.errors()[0]["msg"]
        print(error_message)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()


# pydantic: data validation library that uses Python type hints
# to automatically validate data at runtime

# BaseModel: base class for all Pydantic models

# Field() lets you add validdatoin rules and metadata
# min_length  | minimum string length
# max_length  | maximum string length
# gt          | greater than
# ge          | greater or equal
# lt          | less than
# le          | less or equal
# default     | default value
# ...         | required and has no default value
# description | documentation

# datetime(year, month, day): creates a date
