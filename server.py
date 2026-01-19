from flask import Flask
from app.db.database import db
from app.routes.auth import auth_bp
from app.routes.tasks import task_bp
from app.routes.users import user_bp
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from flask import jsonify



def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///task.db"
    app.config["JWT_SECRET_KEY"] = "super-secret"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 900
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 604800

    db.init_app(app)
    jwt = JWTManager(app)

    

    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["100 per 15 minutes"],
        strategy="moving-window"
    )

    @app.route("/", methods=["GET"])
    def home():
        return jsonify({ 
            "message": "Task Management API is running",
            
        }), 200


    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(task_bp, url_prefix="/api/v1/tasks")
    app.register_blueprint(user_bp, url_prefix="/api/v1/users")

    with app.app_context():
        db.create_all()
       
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
