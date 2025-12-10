from datetime import date, datetime, timedelta
from typing import TYPE_CHECKING

from app import db
from app.models.enums import FrequencyType, HabitIcon, HabitType

if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model
else:
    Model = db.Model


class Habit(Model):
    """Habit model representing user habits"""

    __tablename__ = "habits"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    deadline_time = db.Column(db.Time, nullable=True)
    frequency = db.Column(
        db.Enum(FrequencyType, native_enum=False),
        nullable=False,
        default=FrequencyType.DAILY.value,
    )
    icon = db.Column(
        db.Enum(HabitIcon, native_enum=False),
        nullable=True,
        default=HabitIcon.STAR.value,
    )
    type = db.Column(
        db.Enum(HabitType, native_enum=False),
        nullable=True,
        default=HabitType.WATER.value,
    )
    active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    color = db.Column(db.String(10), nullable=True)

    # Relationships
    tasks = db.relationship(
        "HabitTask", back_populates="habit", cascade="all, delete-orphan"
    )
    statistics = db.relationship(
        "HabitStatistics",
        back_populates="habit",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def is_completed_for_period(self):
        """Check if habit is completed for the current period based on frequency"""
        from sqlalchemy import func

        today = date.today()

        # Define the start date for the period based on frequency
        if self.frequency == FrequencyType.DAILY:
            # Check if completed today
            start_date = today
        elif self.frequency == FrequencyType.WEEKLY:
            # Check if completed this week (Monday-Sunday)
            start_date = today - timedelta(days=today.weekday())
        elif self.frequency == FrequencyType.MONTHLY:
            # Check if completed this month
            start_date = today.replace(day=1)
        elif self.frequency in [
            FrequencyType.EVERY_30_MIN,
            FrequencyType.HOURLY,
            FrequencyType.EVERY_3_HOURS,
            FrequencyType.EVERY_6_HOURS,
        ]:
            # For time-based frequencies, check today
            start_date = today
        else:
            start_date = today

        # Query for completed tasks in the current period
        completed_task = (
            db.session.query(func.count(HabitTask.id))
            .filter(
                HabitTask.habit_id == self.id,
                HabitTask.date >= start_date,
                HabitTask.date <= today,
                HabitTask.completed == True,
            )
            .scalar()
        )

        return completed_task > 0

    def to_dict(self, include_completion_status=False):
        """Convert habit to dictionary"""
        result = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "deadline_time": self.deadline_time.isoformat()
            if self.deadline_time
            else None,
            "frequency": self.frequency,
            "icon": self.icon,
            "type": self.type,
            "active": self.active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "color": self.color,
        }

        if include_completion_status:
            result["is_completed"] = self.is_completed_for_period()

        return result

    def __repr__(self):
        return f"<Habit {self.id}: {self.name}>"


class HabitTask(Model):
    """Habit task model representing scheduled occurrences"""

    __tablename__ = "habit_tasks"

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey("habits.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    completion_time = db.Column(db.DateTime, nullable=True)

    # Relationships
    habit = db.relationship("Habit", back_populates="tasks")

    def to_dict(self):
        """Convert task to dictionary"""
        return {
            "id": self.id,
            "habit_id": self.habit_id,
            "date": self.date.isoformat() if self.date else None,
            "completed": self.completed,
            "completion_time": self.completion_time.isoformat()
            if self.completion_time
            else None,
        }

    def __repr__(self):
        return f"<HabitTask {self.id}: Habit {self.habit_id} on {self.date}>"


class HabitStatistics(Model):
    """Habit statistics model for aggregated data"""

    __tablename__ = "habit_statistics"

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey("habits.id"), nullable=False)
    total_completions = db.Column(db.Integer, default=0, nullable=False)
    current_streak = db.Column(db.Integer, default=0, nullable=False)
    best_streak = db.Column(db.Integer, default=0, nullable=False)
    success_rate = db.Column(db.Float, default=0.0, nullable=False)
    last_completed = db.Column(db.Date, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    habit = db.relationship("Habit", back_populates="statistics")

    def to_dict(self):
        """Convert statistics to dictionary"""
        return {
            "id": self.id,
            "habit_id": self.habit_id,
            "total_completions": self.total_completions,
            "current_streak": self.current_streak,
            "best_streak": self.best_streak,
            "success_rate": self.success_rate,
            "last_completed": self.last_completed.isoformat()
            if self.last_completed
            else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<HabitStatistics {self.id}: Habit {self.habit_id}>"
