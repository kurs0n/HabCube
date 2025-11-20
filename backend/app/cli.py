"""Flask CLI commands for database seeding and maintenance"""
import datetime
import random

import click
from flask.cli import with_appcontext

from app import db
from app.models.enums import FrequencyType, HabitIcon, HabitType
from app.models.habit import Habit, HabitStatistics


@click.command("seed")
@with_appcontext
def seed_db():
    """Seed the database with sample data (soft reset - deactivates existing habits)"""
    from app.models.habit import HabitTask

    existing_count = db.session.query(Habit).count()

    if existing_count > 0:
        click.echo(f"Soft resetting {existing_count} existing habits...")
        # Delete all tasks
        tasks_deleted = db.session.query(HabitTask).delete()
        click.echo(f"✓ Deleted {tasks_deleted} habit tasks")

        # Deactivate all habits
        db.session.query(Habit).update({"active": False})

        # Reset statistics
        db.session.query(HabitStatistics).update({
            "total_completions": 0,
            "current_streak": 0,
            "best_streak": 0,
            "last_completed": None,
            "success_rate": 0.0
        })
        db.session.commit()
        click.echo("✓ Existing habits deactivated and reset.")

    click.echo("Seeding database with sample habits...")
    frequencies = [freq.name for freq in FrequencyType]  # Use enum names (uppercase)
    colors = ["red", "blue", "green", "yellow", "purple", "orange", "gray"]
    icons = [icon.value for icon in HabitIcon]  # Get all available icons
    types = [habit_type.value for habit_type in HabitType]  # Get all available types

    for i in range(1, 61):
        freq = random.choice(frequencies)
        habit = Habit(
            name=f"Habit {i}",
            description=f"Description for habit {i}",
            frequency=freq,
            icon=random.choice(icons),
            type=random.choice(types),
            active=bool(random.getrandbits(1)),
            deadline_time=datetime.time(
                hour=random.randint(0, 23), minute=random.choice([0, 15, 30, 45])
            ),
            color=random.choice(colors),
        )
        db.session.add(habit)
        db.session.flush()

        stats = HabitStatistics(
            habit_id=habit.id,
            total_completions=random.randint(0, 100),
            current_streak=random.randint(0, 20),
            best_streak=random.randint(0, 30),
        )
        db.session.add(stats)

    db.session.commit()
    click.echo("✓ Seeded habits with statistics.")


def init_app(app):
    """Register CLI commands with the Flask app"""
    app.cli.add_command(seed_db)
