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


class TestGetActiveHabits:
    """Test GET /api/v1/habits/active endpoint with frequency filtering"""

    def test_get_active_habits_never_completed(self, client, app):
        """Test that habits never completed are always ready"""
        with app.app_context():
            habit = Habit(name="New Habit", frequency="daily", active=True)
            db.session.add(habit)
            db.session.commit()

        response = client.get("/api/v1/habits/active")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["habits"]) == 1
        assert data["habits"][0]["name"] == "New Habit"

    def test_get_active_habits_daily_completed_today(self, client, app):
        """Test that daily habit completed today is NOT in active list"""
        with app.app_context():
            from app.models.habit import HabitTask

            habit = Habit(name="Daily Habit", frequency="daily", active=True)
            db.session.add(habit)
            db.session.flush()

            # Complete it today
            task = HabitTask(
                habit_id=habit.id,
                date=datetime.date.today(),
                completed=True,
                completion_time=datetime.datetime.utcnow()
            )
            db.session.add(task)
            db.session.commit()

        response = client.get("/api/v1/habits/active")
        assert response.status_code == 200
        data = response.get_json()
        # Should be empty because completed today
        assert len(data["habits"]) == 0

    def test_get_active_habits_daily_completed_yesterday(self, client, app):
        """Test that daily habit completed yesterday IS in active list"""
        with app.app_context():
            from app.models.habit import HabitTask

            habit = Habit(name="Daily Habit", frequency="daily", active=True)
            db.session.add(habit)
            db.session.flush()

            # Complete it yesterday
            yesterday = datetime.date.today() - datetime.timedelta(days=1)
            task = HabitTask(
                habit_id=habit.id,
                date=yesterday,
                completed=True,
                completion_time=datetime.datetime.utcnow() - datetime.timedelta(days=1)
            )
            db.session.add(task)
            db.session.commit()

        response = client.get("/api/v1/habits/active")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["habits"]) == 1
        assert data["habits"][0]["name"] == "Daily Habit"

    def test_get_active_habits_hourly_not_ready(self, client, app):
        """Test that hourly habit completed 30 minutes ago is NOT ready"""
        with app.app_context():
            from app.models.habit import HabitTask

            habit = Habit(name="Hourly Habit", frequency="hourly", active=True)
            db.session.add(habit)
            db.session.flush()

            # Complete it 30 minutes ago
            thirty_min_ago = datetime.datetime.utcnow() - datetime.timedelta(minutes=30)
            task = HabitTask(
                habit_id=habit.id,
                date=datetime.date.today(),
                completed=True,
                completion_time=thirty_min_ago
            )
            db.session.add(task)
            db.session.commit()

        response = client.get("/api/v1/habits/active")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["habits"]) == 0

    def test_get_active_habits_hourly_ready(self, client, app):
        """Test that hourly habit completed 90 minutes ago IS ready"""
        with app.app_context():
            from app.models.habit import HabitTask

            habit = Habit(name="Hourly Habit", frequency="hourly", active=True)
            db.session.add(habit)
            db.session.flush()

            # Complete it 90 minutes ago
            ninety_min_ago = datetime.datetime.utcnow() - datetime.timedelta(minutes=90)
            task = HabitTask(
                habit_id=habit.id,
                date=datetime.date.today(),
                completed=True,
                completion_time=ninety_min_ago
            )
            db.session.add(task)
            db.session.commit()

        response = client.get("/api/v1/habits/active")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["habits"]) == 1
        assert data["habits"][0]["name"] == "Hourly Habit"

    def test_get_active_habits_inactive_not_returned(self, client, app):
        """Test that inactive habits are not returned"""
        with app.app_context():
            habit = Habit(name="Inactive Habit", frequency="daily", active=False)
            db.session.add(habit)
            db.session.commit()

        response = client.get("/api/v1/habits/active")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["habits"]) == 0

    def test_get_active_habits_weekly_ready(self, client, app):
        """Test that weekly habit completed 8 days ago IS ready"""
        with app.app_context():
            from app.models.habit import HabitTask

            habit = Habit(name="Weekly Habit", frequency="weekly", active=True)
            db.session.add(habit)
            db.session.flush()

            # Complete it 8 days ago
            eight_days_ago = datetime.date.today() - datetime.timedelta(days=8)
            task = HabitTask(
                habit_id=habit.id,
                date=eight_days_ago,
                completed=True,
                completion_time=datetime.datetime.utcnow() - datetime.timedelta(days=8)
            )
            db.session.add(task)
            db.session.commit()

        response = client.get("/api/v1/habits/active")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["habits"]) == 1
        assert data["habits"][0]["name"] == "Weekly Habit"

    def test_get_active_habits_mixed_frequencies(self, client, app):
        """Test multiple habits with different frequencies and completion states"""
        with app.app_context():
            from app.models.habit import HabitTask

            # Ready: Daily habit completed yesterday
            habit1 = Habit(name="Ready Daily", frequency="daily", active=True)
            db.session.add(habit1)
            db.session.flush()
            task1 = HabitTask(
                habit_id=habit1.id,
                date=datetime.date.today() - datetime.timedelta(days=1),
                completed=True,
                completion_time=datetime.datetime.utcnow() - datetime.timedelta(days=1)
            )
            db.session.add(task1)

            # Not ready: Hourly completed 30 min ago
            habit2 = Habit(name="Not Ready Hourly", frequency="hourly", active=True)
            db.session.add(habit2)
            db.session.flush()
            task2 = HabitTask(
                habit_id=habit2.id,
                date=datetime.date.today(),
                completed=True,
                completion_time=datetime.datetime.utcnow() - datetime.timedelta(minutes=30)
            )
            db.session.add(task2)

            # Ready: Never completed
            habit3 = Habit(name="Never Completed", frequency="daily", active=True)
            db.session.add(habit3)

            # Not returned: Inactive
            habit4 = Habit(name="Inactive", frequency="daily", active=False)
            db.session.add(habit4)

            db.session.commit()

        response = client.get("/api/v1/habits/active")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["habits"]) == 2
        habit_names = [h["name"] for h in data["habits"]]
        assert "Ready Daily" in habit_names
        assert "Never Completed" in habit_names
        assert "Not Ready Hourly" not in habit_names
        assert "Inactive" not in habit_names

    def test_complete_habit_removes_from_active_daily(self, client, app):
        """Test that completing a daily habit removes it from active list until next day"""
        with app.app_context():
            habit = Habit(name="Daily Task", frequency="daily", active=True)
            db.session.add(habit)
            db.session.flush()

            # Create statistics
            stats = HabitStatistics(habit_id=habit.id)
            db.session.add(stats)
            db.session.commit()
            habit_id = habit.id

        # Step 1: Habit should be in active list (never completed)
        response = client.get("/api/v1/habits/active")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["habits"]) == 1
        assert data["habits"][0]["name"] == "Daily Task"

        # Step 2: Complete the habit
        response = client.post(f"/api/v1/habits/{habit_id}/complete")
        assert response.status_code == 200

        # Step 3: Habit should NOT be in active list anymore (completed today)
        response = client.get("/api/v1/habits/active")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["habits"]) == 0

        # Step 4: Simulate next day by updating the task date to yesterday
        with app.app_context():
            from app.models.habit import HabitTask
            task = HabitTask.query.filter_by(habit_id=habit_id).first()
            task.date = datetime.date.today() - datetime.timedelta(days=1)
            task.completion_time = datetime.datetime.utcnow() - datetime.timedelta(days=1)
            db.session.commit()

        # Step 5: Habit should be back in active list (new day)
        response = client.get("/api/v1/habits/active")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["habits"]) == 1
        assert data["habits"][0]["name"] == "Daily Task"

    def test_complete_habit_removes_from_active_hourly(self, client, app):
        """Test that completing an hourly habit removes it from active list for 1 hour"""
        with app.app_context():
            habit = Habit(name="Hourly Task", frequency="hourly", active=True)
            db.session.add(habit)
            db.session.flush()

            # Create statistics
            stats = HabitStatistics(habit_id=habit.id)
            db.session.add(stats)
            db.session.commit()
            habit_id = habit.id

        # Step 1: Habit should be in active list
        response = client.get("/api/v1/habits/active")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["habits"]) == 1

        # Step 2: Complete the habit
        response = client.post(f"/api/v1/habits/{habit_id}/complete")
        assert response.status_code == 200

        # Step 3: Should NOT be in active list (just completed)
        response = client.get("/api/v1/habits/active")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["habits"]) == 0

        # Step 4: Simulate 90 minutes passing
        with app.app_context():
            from app.models.habit import HabitTask
            task = HabitTask.query.filter_by(habit_id=habit_id).first()
            task.completion_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=90)
            db.session.commit()

        # Step 5: Should be back in active list (90 minutes passed)
        response = client.get("/api/v1/habits/active")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["habits"]) == 1
        assert data["habits"][0]["name"] == "Hourly Task"

    def test_complete_habit_twice_same_day_rejected(self, client, app):
        """Test that completing the same habit twice on the same day is rejected"""
        with app.app_context():
            habit = Habit(name="Daily Task", frequency="daily", active=True)
            db.session.add(habit)
            db.session.flush()

            # Create statistics
            stats = HabitStatistics(habit_id=habit.id)
            db.session.add(stats)
            db.session.commit()
            habit_id = habit.id

        # Complete once - should work
        response = client.post(f"/api/v1/habits/{habit_id}/complete")
        assert response.status_code == 200

        # Complete again - should fail
        response = client.post(f"/api/v1/habits/{habit_id}/complete")
        assert response.status_code == 400
        data = response.get_json()
        assert "already completed today" in data["error"].lower()

        # Should still not be in active list
        response = client.get("/api/v1/habits/active")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["habits"]) == 0
