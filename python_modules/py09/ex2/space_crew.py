from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime
from enum import Enum


class Rank(str, Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True

    def member_info(self) -> None:
        print(f"- {self.name} ({self.rank}) - {self.specialization}")


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def mission_validation(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        has_leader = False
        for cm in self.crew:
            if cm.rank == Rank.commander or cm.rank == Rank.captain:
                has_leader = True
        if not has_leader:
            raise ValueError(
                "Mission must have at least one Commander or Captain")

        if self.duration_days > 365:
            experienced_count = sum(
                1 for c in self.crew if c.years_experience >= 5)
            if (experienced_count / len(self.crew)) < 0.5:
                raise ValueError("Long missions (> 365 days) need 50% "
                                 "experienced crew (5+ years)")

        if not all(c.is_active for c in self.crew):
            raise ValueError("All crew members must be active")

        return self

    def mission_info(self) -> None:
        print("Valid mission created:")
        print(f"Mission: {self.mission_name}")
        print(f"ID: {self.mission_id}")
        print(f"Destination: {self.destination}")
        print(f"Duration: {self.duration_days} days")
        print(f"Budget: ${self.budget_millions}M")
        print(f"Crew size: {len(self.crew)}")
        print("Crew members:")
        for member in self.crew:
            member.member_info()


def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 40)
    try:
        member1 = CrewMember(
            member_id="CM01",
            name="Sarah Connor",
            rank=Rank.commander,
            age=43,
            specialization="Mission Command",
            years_experience=15,
            is_active=True
        )

        member2 = CrewMember(
            member_id="CM02",
            name="John Smith",
            rank=Rank.lieutenant,
            age=58,
            specialization="Navigation",
            years_experience=30,
            is_active=True
        )

        member3 = CrewMember(
            member_id="CM03",
            name="Alice Johnson",
            rank=Rank.officer,
            age=25,
            specialization="Engineering",
            years_experience=5,
            is_active=True
        )

        mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime(2024, 2, 1),
            duration_days=900,
            crew=[member1, member2, member3],
            mission_status="planned",
            budget_millions=2500
        )

        mission.mission_info()
        print()

        print("=" * 40)
        print("Expected validation error:")

        member4 = CrewMember(
            member_id="CM03",
            name="Ed Sheeran",
            rank=Rank.officer,
            age=35,
            specialization="Engineering",
            years_experience=6,
            is_active=True
        )

        mission2 = SpaceMission(
            mission_id="M2024_MOON",
            mission_name="Moon Colony Establishment",
            destination="Moon",
            launch_date=datetime(2024, 12, 31),
            duration_days=90,
            crew=[member4],
            mission_status="planned",
            budget_millions=200
        )

        mission2.mission_info()

    except ValidationError as e:
        error_message = e.errors()[0]["msg"]
        print(error_message.replace("Value error, ", ""))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
