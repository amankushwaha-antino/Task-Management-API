from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.task import Task
from app.db.database import db
from app.middleware.auth import current_user

task_bp = Blueprint("tasks", __name__)


@task_bp.post("")
@jwt_required()
def create_task():
    user = current_user()
    if not user:
        return jsonify(error="Unauthorized"), 401
    data = request.get_json() or {}

    if not data.get("title") or not isinstance(data.get("title"), str):
        return jsonify(error="Title is required and must be a string"), 400

    task = Task(
        title=data["title"],
        description=data.get("description"),
        status=data.get("status", "pending"),
        priority=data.get("priority"),
        due_date=data.get("dueDate"),
        assignee=data.get("assignee"),
        created_by=user.id
    )

    db.session.add(task)
    db.session.commit()
    return jsonify(message="Task created"), 201


@task_bp.get("")
@jwt_required()
def get_tasks():
    user = current_user()
    if not user:
        return jsonify(error="Unauthorized"), 401

    query = Task.query

    if user.role != "admin":
        query = query.filter(
            (Task.created_by == user.id) | (Task.assignee == user.id)
        )

    status = request.args.get("status")
    priority = request.args.get("priority")
    search = request.args.get("search")

    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if search:
        query = query.filter(Task.title.contains(search))

    tasks = query.all()

    return jsonify([
        {
            "id": t.id,
            "title": t.title,
            "status": t.status,
            "priority": t.priority,
            "createdBy": t.created_by,
            "assignee": t.assignee
        } for t in tasks
    ])


@task_bp.get("/<int:id>")
@jwt_required()
def get_task(id):
    user = current_user()
    if not user:
        return jsonify(error="Unauthorized"), 401
    task = Task.query.get_or_404(id)

    if user.role != "admin" and user.id not in [task.created_by, task.assignee]:
        return jsonify(error="You can't see this task"), 403

    return jsonify(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority
    )


@task_bp.put("/<int:id>")
@jwt_required()
def update_task(id):
    user = current_user()
    if not user:
        return jsonify(error="Unauthorized"), 401
    task = Task.query.get(id)
    if not task:
        return jsonify(error="Task not found"), 404
    data = request.get_json() or {}

    if user.role == "admin" or task.created_by == user.id:
        for key in ["title", "description", "status", "priority", "due_date", "assignee"]:
            if key in data:
                setattr(task, key, data[key])

    elif task.assignee == user.id:
        if "status" in data:
            task.status = data["status"]
        else:
            return jsonify(error="Only status update allowed"), 403
    else:
        return jsonify(error="This is not your task"), 403

    db.session.commit()
    return jsonify(message="Task updated")


@task_bp.delete("/<int:id>")
@jwt_required()
def delete_task(id):
    user = current_user()
    if not user:
        return jsonify(error="Unauthorized"), 401
    task = Task.query.get(id)

    if not task:
        return jsonify(error="Task not found"), 404

    if user.role != "admin" and task.created_by != user.id:
        return jsonify(error="You do not have permission to delete this task"), 403

    db.session.delete(task)
    db.session.commit()
    return jsonify(message="Task deleted")


@task_bp.get("stats")
@jwt_required()
def task_stats():
    user = current_user()
    if not user:
        return jsonify(error="Unauthorized"), 401
    query = Task.query

    if user.role != "admin":
        query = query.filter(Task.created_by == user.id)

    total = query.count()
    completed = query.filter(Task.status == "completed").count()
    pending = query.filter(Task.status == "pending").count()

    by_priority = {
        "high": query.filter(Task.priority == "high").count(),
        "medium": query.filter(Task.priority == "medium").count(),
        "low": query.filter(Task.priority == "low").count()
    }

    return jsonify(
        total=total,
        completed=completed,
        pending=pending,
        byPriority=by_priority
    )

