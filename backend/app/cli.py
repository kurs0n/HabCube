"""Flask CLI commands for database seeding and maintenance"""
import datetime
import random

import click
from flask.cli import with_appcontext

from app import db
from app.models.enums import FrequencyType
from app.models.habit import Habit, HabitStatistics


@click.command("seed")
@with_appcontext
def seed_db():
    """Seed the database with sample data (always clears existing data first)"""
    existing_count = db.session.query(Habit).count()

    if existing_count > 0:
        click.echo(f"Clearing {existing_count} existing habits...")
        db.session.query(HabitStatistics).delete()
        db.session.query(Habit).delete()
        db.session.commit()
        click.echo("✓ Existing data cleared.")

    # Reset auto-increment sequences to start from 1
    click.echo("Resetting ID sequences...")
    db.session.execute(db.text("ALTER SEQUENCE habits_id_seq RESTART WITH 1"))
    db.session.execute(db.text("ALTER SEQUENCE habit_statistics_id_seq RESTART WITH 1"))
    db.session.commit()
    click.echo("✓ ID sequences reset.")

    click.echo("Seeding database with sample habits...")
    frequencies = [freq.name for freq in FrequencyType]  # Use enum names (uppercase)
    colors = ["red", "blue", "green", "yellow", "purple", "orange", "gray"]

    for i in range(1, 61):
        freq = random.choice(frequencies)
        habit = Habit(
            name=f"Habit {i}",
            description=f"Description for habit {i}",
            frequency=freq,
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
