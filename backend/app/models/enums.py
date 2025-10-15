from enum import Enum


class FrequencyType(str, Enum):
    """Frequency types for habits"""

    EVERY_30_MIN = "every_30_min"
    HOURLY = "hourly"
    EVERY_3_HOURS = "every_3_hours"
    EVERY_6_HOURS = "every_6_hours"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

    @classmethod
    def choices(cls):
        """Return list of all frequency choices"""
        return [freq.value for freq in cls]

    @classmethod
    def is_valid(cls, value):
        """Check if value is a valid frequency"""
        return value in cls.choices()

    def __str__(self):
        return self.value
