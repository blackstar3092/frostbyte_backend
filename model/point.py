from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# User model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    quiz_scores = db.relationship('QuizScore', back_populates='user')

    def create(self):
        db.session.add(self)
        db.session.commit()

    def read(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

# QuizScore model
class QuizScore(db.Model):
    __tablename__ = 'quiz_scores'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    park = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', back_populates='quiz_scores')

    def create(self):
        db.session.add(self)
        db.session.commit()

    def read(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "points": self.points,
            "park": self.park,
            "timestamp": self.timestamp.isoformat()
        }

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

# Utility function to initialize the database with sample data
def init_db():
    from app import app
    with app.app_context():
        db.create_all()

        # Add sample users
        sample_users = [
            User(username="user1", email="user1@example.com", password="hashed_password1"),
            User(username="user2", email="user2@example.com", password="hashed_password2"),
            User(username="user3", email="user3@example.com", password="hashed_password3")
        ]

        for user in sample_users:
            db.session.add(user)

        db.session.commit()

        # Add sample quiz scores
        sample_scores = [
            QuizScore(user_id=1, points=150, park="Grand Canyon National Park"),
            QuizScore(user_id=2, points=180, park="Redwood National Park"),
            QuizScore(user_id=3, points=230, park="Buck Island Reef National Monument")
        ]

        for score in sample_scores:
            db.session.add(score)

        db.session.commit()

if __name__ == "__main__":
    init_db()
