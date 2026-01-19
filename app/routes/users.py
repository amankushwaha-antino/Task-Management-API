from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.middleware.role import require_roles
from app.models.user import User
from app.db.database import db

user_bp = Blueprint("users", __name__)

@user_bp.delete("/<int:id>")
@jwt_required()
def delete_user(id):
    require_roles("admin")()
    user = User.query.get(id)
    if not user:
        return jsonify(error="User not found"), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify(message="User deleted")


@user_bp.put("/<int:id>")
@jwt_required()
def update_user_role(id):
    require_roles("admin")()

    data = request.json
    new_role = data.get("role")

    if new_role not in ["admin", "user"]:
        return jsonify(error="Invalid role"), 400

    user = User.query.get(id)
    if not user:
        return jsonify(error="User not found"), 404

    user.role = new_role
    db.session.commit()

    return jsonify(
        message="User role updated",
        user_id=user.id,
        role=user.role
    ), 200
