from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from __init__ import db, app  # Ensure these imports are correct

# Helper Functions

def current_timestamp():
    # Returns the current timestamp in UTC.
    # Returns:
    #     datetime: The current UTC datetime.
    return datetime.utcnow()

# Database Models

class AIMessage(db.Model):
    # AIMessage Model
    # This class represents the AIMessage model, which is used to manage actions in the 'ai_messages' table of the database. 
    # It allows storing and managing messages from an AI system, including the timestamp, author, and message category.

    __tablename__ = 'ai_messages'  # Define the table name for the SQLAlchemy model

    # Define the columns for the ai_messages table
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    message = db.Column(db.Text, nullable=False)  # Message content
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Timestamp of the message creation
    author = db.Column(db.String(50), nullable=False, default="AI")  # Author of the message
    category = db.Column(db.String(50), nullable=False, default="response")  # Category of the message

    def __init__(self, message, author="AI", category="response"):
        # Initialize the AIMessage object with provided message, author, and category.
        self.message = message
        self.author = author
        self.category = category


    def get_id(self):
        # Returns the ID of the AI message as a string.
        return str(self.id)
    
    def create(self):
        # Save the AI message to the database.
        db.session.add(self)
        db.session.commit()

    def read(self):
        # Convert the AI message object to a dictionary for JSON serialization.
        # This dictionary represents a row in the database, with keys as column names and values as the corresponding data.
        return {
            "id": self.id,  # Column: id
            "message": self.message,  # Column: message
            "timestamp": self.timestamp.isoformat(),  # Column: timestamp
            "author": self.author,  # Column: author
            "category": self.category  # Column: category
        }

    def update(self, updates):
        # Updates the AIMessage object with provided updates.
        # Args:
        #     updates (dict): A dictionary containing the new data for the message.
        # Returns:
        #     AIMessage: The updated AIMessage object, or None on error.
        if not isinstance(updates, dict):
            return self
        
        # Iterate over the dictionary items and update the corresponding attributes
        for key, value in updates.items():
            if hasattr(self, key) and key != "id":  # Avoid updating the primary key
                setattr(self, key, value)

        try:
            db.session.commit()  # Commit the changes to the database
            return self
        except IntegrityError:
            db.session.rollback()  # Rollback the changes on error
            return None

    def delete(self):
        # Deletes the AIMessage object from the database.
        # Returns:
        #     None
        db.session.delete(self)
        db.session.commit()

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
