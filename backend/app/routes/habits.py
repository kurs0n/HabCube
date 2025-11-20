import os
from datetime import date, datetime

from flask import Blueprint, jsonify, request
from sqlalchemy import func

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


@habits_bp.route("/finished-habits", methods=["GET"])
@swag_from(os.path.join(DOCS_DIR, "finished_habits.yml"))
def get_finished_habits():
    try:
        habits = Habit.query.filter_by(active=False).all()
        finished_habits = []
        for habit in habits:
            finished_habit = {}
            habit_dict = habit.to_dict()
            finished_habit["id"] = habit_dict["id"]
            finished_habit["name"] = habit_dict["name"]
            finished_habit["description"] = habit_dict["description"]
            finished_habit["icon"] = habit_dict["icon"]

            if habit.statistics:
                stats_data = habit.statistics.to_dict()
                best_streak = stats_data.get("best_streak", 0)
                finished_habit["best_streak"] = best_streak
                if int(best_streak) >= 21:
                    finished_habit["success_status"] = True
                else:
                    finished_habit["success_status"] = False
                finished_habit["finish_date"] = stats_data["last_completed"]
            else:
                finished_habit["best_streak"] = 0
                finished_habit["success_status"] = False
                finished_habit["finish_date"] = ''

            finished_habits.append(finished_habit)

        return jsonify({"habits": finished_habits}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": f"Failed to fetch habits: {str(e)}"}), 500

@habits_bp.route("/statistics", methods=["GET"])
def get_habits_statistics():
    try:
        total_habits = db.session.query(func.count(Habit.id)).scalar()

        active_habits_count = db.session.query(Habit).filter_by(active=True).count()
        inactive_habits_count = total_habits - active_habits_count

        longest_streak = db.session.query(func.max(HabitStatistics.best_streak)).scalar()

        if longest_streak is None:
            longest_streak = 0

        average_completion_rate = db.session.query(
            func.avg(HabitStatistics.success_rate)
        ).scalar()

        if average_completion_rate is None:
            average_completion_rate = 0.0
        else:
            average_completion_rate = round(average_completion_rate, 2)

        response_data = {
            "total_habits": total_habits,
            "active_habits_count": active_habits_count,
            "completed_habits_count": inactive_habits_count,
            "longest_streak": longest_streak,
            "average_completion_rate": average_completion_rate
        }

        return jsonify(response_data), 200

    except Exception as e:
        print(f"Error fetching global statistics: {e}")
        return jsonify({"error": f"Failed to fetch statistics: {str(e)}"}), 500


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
