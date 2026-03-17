from pydantic import BaseModel, Field, model_validator, ValidationError
# @model_validator(mode='before') vs (mode='after')
# before: before pydantic parses fields
# after: runs after validation and parsing
from datetime import datetime
from enum import Enum


# Enums in python are used to define a set of named constant values
class ContactType(str, Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def validation_rules(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")

        if self.contact_type == ContactType.physical and not self.is_verified:
            raise ValueError("Physical contact must be verified")

        if self.contact_type == ContactType.telepathic \
           and self.witness_count < 3:
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses")

        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError(
                "Strong signals (>7.0) must include a received message")
        return self

    def log_validation(self) -> None:
        print("Valid contact report:")
        print(f"ID: {self.contact_id}")
        print(f"Type: {self.contact_type}")
        print(f"Location: {self.location}")
        print(f"Signal: {self.signal_strength}/10")
        print(f"Duration: {self.duration_minutes} minutes")
        print(f"Witnesses: {self.witness_count}")
        print(f"Message: '{self.message_received}'")
        print()


def main() -> None:
    print("Alien Contact Log Validation")
    print("=" * 40)
    try:
        log = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime(2024, 11, 12),
            location="Area 51, Nevada",
            contact_type=ContactType.radio,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticulli",
            is_verified=True
        )
        log.log_validation()

        print("=" * 40)
        print("Expected validation error:")

        log = AlienContact(
            contact_id="AC_2026_012",
            timestamp=datetime(2026, 3, 12),
            location="Area 3, Heilbronn",
            contact_type=ContactType.telepathic,
            signal_strength=9.5,
            duration_minutes=20,
            witness_count=1,
            message_received="Greetings from 42",
            is_verified=True
        )
        log.log_validation()
    except ValidationError as e:
        error_message = e.errors()[0]["msg"]
        print(error_message.replace("Value error, ", ""))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
