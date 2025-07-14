from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, timezone


db = SQLAlchemy()
tz_utc8 = timezone(timedelta(hours=8))

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(tz_utc8))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(tz_utc8), onupdate=lambda: datetime.now(tz_utc8))


    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Todo {self.title}>'