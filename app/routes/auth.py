from flask import Blueprint, request, jsonify
from app.models.user import User
from app.db.database import db
from app.utils.password import hash_password, verify_password
from app.utils.jwt_utils import generate_tokens
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/register")
def register():
    data = request.json
    user = User(
        name=data["name"],
        email=data["email"],
        password=hash_password(data["password"]),
        role=data.get("role", "user")
    )
    if user.query.filter_by(email=data["email"]).first():
        return jsonify(error="User already registered"), 400
    db.session.add(user)
    db.session.commit()
    return jsonify(message="User registered"), 201

@auth_bp.post("/login")
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not verify_password(data["password"], user.password):
        return jsonify(error="Invalid credentials"), 401
    tokens = generate_tokens(user.id)
    return jsonify(tokens)

@auth_bp.post("/logout")
@jwt_required()
def logout():
    return jsonify(
        message=f"User {get_jwt_identity()} logged out successfully"
    ), 200

@auth_bp.get("/me")
@jwt_required()
def profile():
    user = User.query.get(get_jwt_identity())
    return jsonify(id=user.id, name=user.name, email=user.email, role=user.role)

@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    return jsonify(access_token=generate_tokens(identity)["access_token"])
