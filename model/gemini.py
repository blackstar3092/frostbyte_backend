from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from __init__ import db, app  # Ensure these imports are correct

""" Helper Functions """

def current_timestamp():
    """
    Returns the current timestamp in UTC.
    
    Returns:
        datetime: The current UTC datetime.
    """
    return datetime.utcnow()

""" Database Models """

class AIMessage(db.Model):
    """
    AIMessage Model
    
    This class represents the AIMessage model, which is used to manage actions in the 'ai_messages' table of the database. 
    It allows storing and managing messages from an AI system, including the timestamp, author, and message category.

    Attributes:
        __tablename__ (str): Specifies the name of the table in the database.
        id (Column): The primary key, an integer representing the unique identifier for the message.
        message (Column): A text column storing the actual message content.
        timestamp (Column): A DateTime column storing when the message was created.
        author (Column): A string representing the author of the message (defaults to "AI").
        category (Column): A string representing the message category (defaults to "response").
    """
    __tablename__ = 'ai_messages'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=current_timestamp, nullable=False)
    author = db.Column(db.String(50), nullable=False, default="AI")
    category = db.Column(db.String(50), nullable=False, default="response")

    def __init__(self, message, author="AI", category="response"):
        """
        Constructor, initializes the AIMessage object with provided message, author, and category.
        
        Args:
            message (str): The content of the message.
            author (str): The author of the message, defaults to "AI".
            category (str): The category of the message, defaults to "response".
        """
        self.message = message
        self.author = author
        self.category = category

    def get_id(self):
        """
        Returns the message's ID as a string.
        
        Returns:
            str: The message's ID.
        """
        return str(self.id)

    def create(self):
        """
        Creates a new AIMessage record and saves it to the database.
        
        Returns:
            AIMessage: The created AIMessage object, or None on error.
        """
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            return None

    def read(self):
        """
        Converts the AIMessage object to a dictionary.
        
        Returns:
            dict: A dictionary representation of the AIMessage object.
        """
        return {
            "id": self.id,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "author": self.author,
            "category": self.category
        }

    def update(self, updates):
        """
        Updates the AIMessage object with new data.
        
        Args:
            updates (dict): A dictionary containing the new data for the message.
        
        Returns:
            AIMessage: The updated AIMessage object, or None on error.
        """
        if not isinstance(updates, dict):
            return self
        
        for key, value in updates.items():
            if hasattr(self, key) and key != "id":
                setattr(self, key, value)

        try:
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            return None

    def delete(self):
        """
        Deletes the AIMessage object from the database.
        
        Returns:
            None
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

""" Database Initialization """

def initAIMessage():
    """
    The initAIMessage function creates the AIMessage table and adds a sample message to the table if it is empty.
    
    Uses:
        The db ORM methods to create the table.
    
    Raises:
        IntegrityError: An error occurred when adding the sample data to the table.
    """
    with app.app_context():
        """Create database and tables"""
        db.create_all()

        """Sample data for table"""
        if AIMessage.query.first() is None:
            sample_message = AIMessage(
                message="Hello, How Can I help?",
                author="AI"
            )
            try:
                db.session.add(sample_message)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

# Example of finding a message by ID
def find_message_by_id(message_id):
    """
    Finds a message by its ID.
    
    Args:
        message_id (int): The ID of the message to find.
    
    Returns:
        AIMessage: The found AIMessage object, or None if not found.
    """
    with app.app_context():
        return AIMessage.query.filter_by(id=message_id).first()
