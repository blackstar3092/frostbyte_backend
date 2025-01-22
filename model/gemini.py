from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from __init__ import db, app  # Ensure these imports are correct


class AIMessage(db.Model):
    __tablename__ = 'ai_messages'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    author = db.Column(db.String(50), nullable=False, default="AI")
    category = db.Column(db.String(50), nullable=False, default="response")

    def __init__(self, message, author="AI", category="response"):
        self.message = message
        self.author = author
        self.category = category

    def create(self):
        """Create a new AIMessage and save it to the database."""
        db.session.add(self)
        db.session.commit()

    def read(self):
        """Return a dictionary representation of the message."""
        return {
            "id": self.id,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "author": self.author,
            "category": self.category
        }

    def update(self, updates):
        """Update the AIMessage fields."""
        for key, value in updates.items():
            if hasattr(self, key) and key != "id":
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        """Delete the AIMessage from the database."""
        db.session.delete(self)
        db.session.commit()

# Initialize the AIMessage table
def initAIMessage(app):
    with app.app_context():
        db.create_all()
        if AIMessage.query.first() is None:
            sample_message = AIMessage(
                message="Hello, How Can I help?",
                author="AI"
            )
            db.session.add(sample_message)
            db.session.commit()
