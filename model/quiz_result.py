from datetime import datetime
from __init__ import db
from model.frostbyte import Frostbyte  # Assuming Frostbyte is your user model

class QuizResult(db.Model):
    __tablename__ = 'quiz_results'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('frostbytes.id'), nullable=False)  # Link to Frostbyte
    assigned_park = db.Column(db.String(100), nullable=False)  # National park assigned
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # When the quiz was taken

    user = db.relationship('Frostbyte', backref='quiz_results')  # Relationship to Frostbyte

    def __init__(self, user_id, assigned_park):
        self.user_id = user_id
        self.assigned_park = assigned_park
    
    def create(self):
        """Save the quiz result to the database."""
        db.session.add(self)
        db.session.commit()

    def read(self):
        """Convert the quiz result object to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "assigned_park": self.assigned_park,
            "timestamp": self.timestamp.isoformat()
        }

    def update(self, assigned_park=None):
        """Update the quiz result in the database."""
        if assigned_park:
            self.assigned_park = assigned_park
        db.session.commit()

    def delete(self):
        """Delete the quiz result from the database."""
        db.session.delete(self)
        db.session.commit()

# Function to initialize sample quiz results (optional)
def initQuizResults():
    sample_results = [
        {"user_id": 1, "assigned_park": "Denali National Park"},
        {"user_id": 2, "assigned_park": "Grand Canyon National Park"},
    ]
    for data in sample_results:
        result = QuizResult(user_id=data["user_id"], assigned_park=data["assigned_park"])
        db.session.add(result)
    db.session.commit()