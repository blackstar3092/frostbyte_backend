from sqlalchemy.exc import IntegrityError
from __init__ import app, db

class AImessage(db.Model):
    __tablename__ = 'ai_messages'  # Define the table name
    
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    content = db.Column(db.Text, nullable=False)  # Message content
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # Creation timestamp
    author = db.Column(db.String(100), nullable=False)  # Author of the message

    def __init__(self, content, author):
        """Initialize the AIMessage object with content and author."""
        self.content = content
        self.author = author

    def read(self):
        """Return a dictionary representation of the AIMessage object."""
        return {
            "id": self.id,  # Unique ID of the message
            "content": self.content,  # Message text
            "timestamp": self.created_at.isoformat(),  # Timestamp in ISO format
            "author": self.author  # Author of the message
        }

    def update(self, updates):
        """Update the AImessage object with provided updates."""
        for key, value in updates.items():
            if hasattr(self, key) and key != "id":  # Avoid updating primary key
                setattr(self, key, value)
        db.session.commit()  # Save changes to the database

    def delete(self):
        """Delete the AImessage object from the database."""
        db.session.delete(self)
        db.session.commit()
def initAIMessage():
    """
    The initAIMessage function creates the AIMessage table and adds some tester data to the table.
    
    Uses:
        The db ORM methods to create the table.
    
    Instantiates:
        AIMessage objects with tester data.
    
    Raises:
        IntegrityError: An error occurred when adding the tester data to the table.
    """
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        
        """Tester data for AIMessage table"""
        message1 = AImessage(content="Hello, how are you?", author="Assistant")
        message2 = AImessage(content="I am a bot!", author="Bot")
        message3 = AImessage(content="Goodbye, take care!", author="Assistant")

        messages = [message1, message2, message3]
        
        for message in messages:
            try:
                db.session.add(message)  # Add each message to the session
                db.session.commit()       # Commit the transaction to save the message
            except IntegrityError:
                db.session.rollback()      # Rollback in case of error
                print(f"Error adding message: {message.content}")
