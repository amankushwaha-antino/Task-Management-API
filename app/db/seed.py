from app.models.user import User
from app.db.database import db
from app.utils.password import hash_password

def seed_admin():
    admin_email = "admin@test.com"

    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        admin = User(
            name="Admin",
            email=admin_email,
            password=hash_password("admin123"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Default admin created")
    else:
        print("ℹ️ Admin already exists")
