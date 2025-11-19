from dataclasses import dataclass
from datetime import time
from typing import Optional

from app.models.enums import FrequencyType, HabitIcon


@dataclass
class CreateHabitDTO:
    """Data Transfer Object for creating a new habit"""

    name: str
    description: Optional[str] = None
    deadline_time: Optional[time] = None
    frequency: FrequencyType = FrequencyType.DAILY
    icon: Optional[HabitIcon] = HabitIcon.STAR

    @classmethod
    def from_dict(cls, data: dict) -> "CreateHabitDTO":
        """Create DTO from dictionary"""
        return cls(
            name=str(data.get("name", "")),
            description=data.get("description"),
            deadline_time=data.get("deadline_time"),
            frequency=data.get("frequency", FrequencyType.DAILY),
            icon=data.get("icon", HabitIcon.STAR),
        )

    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate the DTO data"""
        if not self.name or not self.name.strip():
            return False, "Name is required and cannot be empty"

        if self.frequency and not FrequencyType.is_valid(self.frequency):
            return (
                False,
                f"Invalid frequency. Must be one of: {', '.join(FrequencyType.choices())}",
            )

        if self.icon and not HabitIcon.is_valid(self.icon):
            return (
                False,
                f"Invalid icon. Must be one of available icons",
            )

        return True, None


@dataclass
class HabitResponseDTO:
    """Data Transfer Object for habit response"""

    id: int
    name: str
    description: Optional[str]
    deadline_time: Optional[str]
    frequency: str
    icon: Optional[str]
    active: bool
    created_at: str
    color: Optional[str]

    @classmethod
    def from_model(cls, habit) -> "HabitResponseDTO":
        """Create DTO from Habit model"""
        return cls(
            id=habit.id,
            name=habit.name,
            description=habit.description,
            deadline_time=habit.deadline_time.isoformat()
            if habit.deadline_time
            else None,
            frequency=habit.frequency,
            icon=habit.icon,
            active=habit.active,
            created_at=habit.created_at.isoformat() if habit.created_at else None,
            color=habit.color,
        )

    def to_dict(self) -> dict:
        """Convert DTO to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "deadline_time": self.deadline_time,
            "frequency": self.frequency,
            "icon": self.icon,
            "active": self.active,
            "created_at": self.created_at,
            "color": self.color,
        }
