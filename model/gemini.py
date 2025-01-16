from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship
from model.post import Post
from __init__ import app, db
from api.jwt_authorize import token_required


class AIMessage(db.Model):
    __tablename__ = 'ai_messages'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    author = db.Column(db.String(100), nullable=False)

    def __init__(self, message, author):
        self.message = message
        self.author = author
        self.timestamp = datetime.utcnow()

    def read(self):
        return {
            "id": self.id,
            "message": self.message,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "author": self.author
        }

    def update(self, updates):
        for key, value in updates.items():
            if hasattr(self, key) and key != "id":  # Prevent modifying the ID
                setattr(self, key, value)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def initAIMessages():
    """
    Initializes the ai_messages table and inserts sample data if it does not exist.
    """
    with app.app_context():  # Ensure we are within the app context
        db.create_all()  # Create all tables if they do not exist

        # Check if data exists to avoid duplicate entries
        if AIMessage.query.first() is None:
            sample_messages = [
                AIMessage(message="Hello, welcome!", author="AI"),
                AIMessage(message="How can I assist you?", author="AI"),
                AIMessage(message="Goodbye! Have a great day!", author="AI")
            ]

            try:
                db.session.bulk_save_objects(sample_messages)  # More efficient bulk insert
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


# Testing operations (should not be in the init function)
def test_operations():
    with app.app_context():
        # Insert a new message
        new_message = AIMessage(message="This is a new test message", author="Tester")
        db.session.add(new_message)
        db.session.commit()

        # Query and print messages
        messages = AIMessage.query.all()
        for msg in messages:
            print(msg.read())

        # Update a message
        msg = AIMessage.query.get(1)  # Get message with ID 1
        if msg:
            msg.update({"message": "Updated message content"})

        # Delete a message
        msg = AIMessage.query.get(1)  # Get message with ID 1
        if msg:
            msg.delete()
