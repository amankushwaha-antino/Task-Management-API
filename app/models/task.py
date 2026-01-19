from app.db.database import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    status = db.Column(db.String(20), default="pending")
    priority = db.Column(db.String(20))
    due_date = db.Column(db.String(50))
    created_by = db.Column(db.Integer, nullable=False)
    assignee = db.Column(db.Integer, nullable=True)
