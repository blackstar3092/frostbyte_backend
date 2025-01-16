from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from __init__ import db, app  # Ensure these imports are correct

class AIMessage(db.Model):
    __tablename__ = 'ai_messages'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    author = db.Column(db.String(50), nullable=False, default="AI")  # "AI" or "User"
    category = db.Column(db.String(50), nullable=False, default="response")
    
    def __init__(self, message, author="AI", category="response"):
        self.message = message
        self.author = author
        self.category = category

    def create(self):
        """Save the AI message to the database."""
        db.session.add(self)
        db.session.commit()

    def read(self):
        """Convert the AI message object to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "author": self.author,
            "category": self.category,
        }

    def update(self, updates):
        """Update AI message fields dynamically."""
        for key, value in updates.items():
            if hasattr(self, key) and key != "id":  # Avoid updating the primary key
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        """Delete the AI message from the database."""
        db.session.delete(self)
        db.session.commit()

def initAIMessage():
    """
    Initializes the ai_messages table and inserts sample data if it does not exist.
    """
    with app.app_context():
        db.create_all()  # Ensure the table exists

        # Check if messages already exist to prevent duplicate entries
        if AIMessage.query.first() is None:
            sample_message = AIMessage(message="Hello, How Can I help?", author="AI")
            db.session.add(sample_message)
            db.session.commit()