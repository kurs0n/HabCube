import os
from datetime import date, datetime

from flask import Blueprint, jsonify, request

from app import db
from app.models.dto import CreateHabitDTO
from app.models.enums import FrequencyType, HabitIcon
from app.models.habit import Habit, HabitStatistics, HabitTask
from app.swagger import swag_from

habits_bp = Blueprint("habits", __name__)

DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")


@habits_bp.route("/habits", methods=["GET"])
@swag_from(os.path.join(DOCS_DIR, "get_habits.yml"))
def get_habits():
    try:
        habits = Habit.query.all()
        return jsonify({"habits": [habit.to_dict() for habit in habits]}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to fetch habits: {str(e)}"}), 500


@habits_bp.route("/habits/active", methods=["GET"])
def get_active_habits():
    """Get active habits that are ready to be completed based on their frequency"""
    try:
        now = datetime.utcnow()
        today = date.today()

        # Get all active habits
        active_habits = Habit.query.filter_by(active=True).all()

        ready_habits = []
        for habit in active_habits:
            # Get last completion
            last_task = HabitTask.query.filter_by(
                habit_id=habit.id,
                completed=True
            ).order_by(HabitTask.completion_time.desc()).first()

            is_ready = False

            if not last_task:
                # Never completed, always ready
                is_ready = True
            else:
                last_completion = last_task.completion_time
                time_diff = now - last_completion

                # Check based on frequency
                if habit.frequency == FrequencyType.EVERY_30_MIN.value:
                    is_ready = time_diff.total_seconds() >= 30 * 60
                elif habit.frequency == FrequencyType.HOURLY.value:
                    is_ready = time_diff.total_seconds() >= 60 * 60
                elif habit.frequency == FrequencyType.EVERY_3_HOURS.value:
                    is_ready = time_diff.total_seconds() >= 3 * 60 * 60
                elif habit.frequency == FrequencyType.EVERY_6_HOURS.value:
                    is_ready = time_diff.total_seconds() >= 6 * 60 * 60
                elif habit.frequency == FrequencyType.DAILY.value:
                    # Ready if last completion was before today
                    is_ready = last_task.date < today
                elif habit.frequency == FrequencyType.WEEKLY.value:
                    # Ready if last completion was 7+ days ago
                    is_ready = (today - last_task.date).days >= 7
                elif habit.frequency == FrequencyType.MONTHLY.value:
                    # Ready if last completion was 30+ days ago
                    is_ready = (today - last_task.date).days >= 30

            if is_ready:
                ready_habits.append(habit.to_dict())

        return jsonify({"habits": ready_habits}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to fetch active habits: {str(e)}"}), 500


@habits_bp.route("/habits/<int:habit_id>", methods=["GET"])
@swag_from(os.path.join(DOCS_DIR, "get_habit.yml"))
def get_habit(habit_id):
    try:
        habit = db.session.get(Habit, habit_id)

        if not habit:
            return jsonify({"error": "Habit not found"}), 404

        response_data = habit.to_dict()

        # Include statistics if available
        if habit.statistics:
            response_data["statistics"] = habit.statistics.to_dict()

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": f"Failed to fetch habit: {str(e)}"}), 500


@habits_bp.route("/habits", methods=["POST"])
@swag_from(os.path.join(DOCS_DIR, "create_habit.yml"))
def create_habit():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Parse deadline_time if provided
        deadline_time = None
        if "deadline_time" in data and data["deadline_time"]:
            try:
                deadline_time = datetime.strptime(data["deadline_time"], "%H:%M").time()
            except ValueError:
                return (
                    jsonify({"error": "Invalid deadline_time format. Use HH:MM"}),
                    400,
                )

        # Validate frequency
        frequency = data.get("frequency", FrequencyType.DAILY.value)
        if not FrequencyType.is_valid(frequency):
            return (
                jsonify(
                    {
                        "error": f"Invalid frequency. Must be one of: {', '.join(FrequencyType.choices())}"
                    }
                ),
                400,
            )

        # Validate icon
        icon = data.get("icon", HabitIcon.STAR.value)
        if icon and not HabitIcon.is_valid(icon):
            return (
                jsonify({"error": "Invalid icon"}),
                400,
            )

        # Create DTO and validate
        dto = CreateHabitDTO(
            name=data.get("name"),
            description=data.get("description"),
            deadline_time=deadline_time,
            frequency=frequency,
            icon=icon,
        )

        is_valid, error_message = dto.validate()
        if not is_valid:
            return jsonify({"error": error_message}), 400

        # Create new habit
        habit = Habit(
            name=dto.name,
            description=dto.description,
            deadline_time=dto.deadline_time,
            frequency=dto.frequency,
            icon=dto.icon,
            active=True,
        )

        db.session.add(habit)
        db.session.flush()

        # Create initial statistics record
        statistics = HabitStatistics(habit_id=habit.id)
        db.session.add(statistics)

        db.session.commit()

        return (
            jsonify(
                {"message": "Habit created successfully", "habit": habit.to_dict()}
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create habit: {str(e)}"}), 500


@habits_bp.route("/habits/<int:habit_id>/complete", methods=["POST"])
@swag_from(os.path.join(DOCS_DIR, "complete_habit.yml"))
def complete_habit(habit_id):
    try:
        habit = db.session.get(Habit, habit_id)

        if not habit:
            return jsonify({"error": "Habit not found"}), 404

        completion_date = date.today()

        # Check if already completed today
        existing_task = HabitTask.query.filter_by(
            habit_id=habit_id, date=completion_date
        ).first()

        if existing_task and existing_task.completed:
            return jsonify({"error": "Habit already completed today"}), 400

        # Create completion task
        task = HabitTask(
            habit_id=habit_id,
            date=completion_date,
            completed=True,
            completion_time=datetime.utcnow(),
        )
        db.session.add(task)

        # Update statistics
        statistics = habit.statistics
        if not statistics:
            statistics = HabitStatistics(habit_id=habit_id)
            db.session.add(statistics)

        statistics.total_completions += 1
        statistics.last_completed = completion_date
        statistics.updated_at = datetime.utcnow()

        # Update streak
        if statistics.total_completions == 1:
            statistics.current_streak = 1
        else:
            # Check previous completion
            previous_task = (
                HabitTask.query.filter_by(habit_id=habit_id, completed=True)
                .filter(HabitTask.date < completion_date)
                .order_by(HabitTask.date.desc())
                .first()
            )
            if previous_task:
                days_diff = (completion_date - previous_task.date).days
                if days_diff == 1:
                    statistics.current_streak += 1
                else:
                    statistics.current_streak = 1
            else:
                statistics.current_streak = 1

        # Update best streak
        if statistics.current_streak > statistics.best_streak:
            statistics.best_streak = statistics.current_streak

        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Habit completed successfully",
                    "task": task.to_dict(),
                    "statistics": statistics.to_dict(),
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to complete habit: {str(e)}"}), 500
