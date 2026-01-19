from flask import abort
from app.middleware.auth import current_user

def require_roles(*roles):
    def wrapper():
        user = current_user()
        if user.role not in roles:
            abort(403)
    return wrapper
