import datetime
import random

import pytest

from app import create_app, db
from app.models.habit import Habit, HabitStatistics


@pytest.fixture(scope="function")
def many_habits(app):
    with app.app_context():
        habits = []
        frequencies = [
            "every_30_min",
            "hourly",
            "every_3_hours",
            "daily",
            "weekly",
            "monthly",
        ]
        colors = ["red", "blue", "green", "yellow", "purple", "orange", "gray"]
        for i in range(1, 51):
            habit = Habit(
                name=f"Habit {i}",
                description=f"Description for habit {i}",
                frequency=random.choice(frequencies),
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
            habits.append(habit.id)
        db.session.commit()
        yield habits


@pytest.fixture
def app():
    """Create and configure a test app instance"""
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()


@pytest.fixture
def sample_habit(app):
    """Create a sample habit for testing"""
    with app.app_context():
        habit = Habit(
            name="Drink water",
            description="Drink 8 glasses of water",
            frequency="daily",
            active=True,
        )
        db.session.add(habit)
        db.session.flush()  # Flush to get the ID

        # Create initial statistics with the ID
        stats = HabitStatistics(habit_id=habit.id)
        db.session.add(stats)

        db.session.commit()

        habit_id = habit.id

        yield habit_id


class TestGetHabits:
    """Test GET /api/v1/habits endpoint"""

    def test_get_empty_habits_list(self, client):
        """Test getting habits when database is empty"""
        response = client.get("/api/v1/habits")
        assert response.status_code == 200
        data = response.get_json()
        assert "habits" in data
        assert len(data["habits"]) == 0

    def test_get_habits_list(self, client, sample_habit):
        """Test getting list of habits"""
        response = client.get("/api/v1/habits")
        assert response.status_code == 200
        data = response.get_json()
        assert "habits" in data
        assert len(data["habits"]) == 1
        habit = data["habits"][0]
        assert habit["name"] == "Drink water"
        assert habit["description"] == "Drink 8 glasses of water"
        assert habit["frequency"] == "daily"
        assert habit["active"] is True


class TestGetHabit:
    """Test GET /api/v1/habits/<id> endpoint"""

    def test_get_existing_habit(self, client, sample_habit):
        """Test getting a specific habit by ID"""
        response = client.get(f"/api/v1/habits/{sample_habit}")
        assert response.status_code == 200
        data = response.get_json()
        assert data["name"] == "Drink water"
        assert data["id"] == sample_habit
        assert "statistics" in data

    def test_get_nonexistent_habit(self, client):
        """Test getting a habit that doesn't exist"""
        response = client.get("/api/v1/habits/999")
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Habit not found"


class TestCreateHabit:
    """Test POST /api/v1/habits endpoint"""

    def test_create_habit_minimal(self, client):
        """Test creating a habit with only required fields"""
        response = client.post(
            "/api/v1/habits",
            json={"name": "Exercise"},
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data["message"] == "Habit created successfully"
        assert data["habit"]["name"] == "Exercise"
        assert data["habit"]["frequency"] == "daily"
        assert data["habit"]["active"] is True

    def test_create_habit_full(self, client):
        """Test creating a habit with all fields"""
        response = client.post(
            "/api/v1/habits",
            json={
                "name": "Meditate",
                "description": "10 minutes of meditation",
                "deadline_time": "21:00",
                "frequency": "daily",
            },
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data["habit"]["name"] == "Meditate"
        assert data["habit"]["description"] == "10 minutes of meditation"
        assert data["habit"]["deadline_time"] == "21:00:00"
        assert data["habit"]["frequency"] == "daily"

    def test_create_habit_with_different_frequencies(self, client):
        """Test creating habits with different frequency types"""
        frequencies = [
            "every_30_min",
            "hourly",
            "every_3_hours",
            "daily",
            "weekly",
            "monthly",
        ]

        for freq in frequencies:
            response = client.post(
                "/api/v1/habits",
                json={
                    "name": f"Habit {freq}",
                    "frequency": freq,
                },
            )
            assert response.status_code == 201
            data = response.get_json()
            assert data["habit"]["frequency"] == freq

    def test_create_habit_missing_name(self, client):
        """Test creating a habit without a name"""
        response = client.post("/api/v1/habits", json={})
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_create_habit_invalid_frequency(self, client):
        """Test creating a habit with invalid frequency"""
        response = client.post(
            "/api/v1/habits",
            json={
                "name": "Test",
                "frequency": "invalid_frequency",
            },
        )
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "frequency" in data["error"].lower()

    def test_create_habit_invalid_time_format(self, client):
        """Test creating a habit with invalid time format"""
        response = client.post(
            "/api/v1/habits",
            json={
                "name": "Test",
                "deadline_time": "25:00",  # Invalid time
            },
        )
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data


class TestCompleteHabit:
    """Test POST /api/v1/habits/<id>/complete endpoint"""

    def test_complete_habit_first_time(self, client, sample_habit):
        """Test completing a habit for the first time"""
        response = client.post(f"/api/v1/habits/{sample_habit}/complete")
        assert response.status_code == 200
        data = response.get_json()
        assert data["message"] == "Habit completed successfully"
        assert "task" in data
        assert data["task"]["completed"] is True
        assert "statistics" in data
        assert data["statistics"]["total_completions"] == 1
        assert data["statistics"]["current_streak"] == 1
        assert data["statistics"]["best_streak"] == 1

    def test_complete_habit_already_completed_today(self, client, sample_habit):
        """Test completing a habit that was already completed today"""
        # Complete once
        client.post(f"/api/v1/habits/{sample_habit}/complete")

        # Try to complete again
        response = client.post(f"/api/v1/habits/{sample_habit}/complete")
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "already completed" in data["error"].lower()

    def test_complete_nonexistent_habit(self, client):
        """Test completing a habit that doesn't exist"""
        response = client.post("/api/v1/habits/999/complete")
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Habit not found"


class TestHabitStatistics:
    """Test habit statistics tracking"""

    def test_streak_tracking(self, client, app, sample_habit):
        """Test that streaks are properly tracked"""
        with app.app_context():
            # Complete habit
            response = client.post(f"/api/v1/habits/{sample_habit}/complete")
            assert response.status_code == 200
            data = response.get_json()
            assert data["statistics"]["current_streak"] == 1
            assert data["statistics"]["best_streak"] == 1
            assert data["statistics"]["total_completions"] == 1

    def test_statistics_in_habit_response(self, client, sample_habit):
        """Test that statistics are included in habit response"""
        # Complete the habit first
        client.post(f"/api/v1/habits/{sample_habit}/complete")

        # Get the habit
        response = client.get(f"/api/v1/habits/{sample_habit}")
        assert response.status_code == 200
        data = response.get_json()
        assert "statistics" in data
        assert data["statistics"]["total_completions"] >= 1
