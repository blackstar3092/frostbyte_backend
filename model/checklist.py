from datetime import datetime
from sqlalchemy.orm import relationship
from __init__ import db


class ChecklistItem(db.Model):
    __tablename__ = 'checklist_items'
   
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  
    item_name = db.Column(db.String(100), nullable=False)
    is_checked = db.Column(db.Boolean, default=False, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


    def __init__(self, user_id, item_name, is_checked=False):
        self.user_id = user_id
        self.item_name = item_name
        self.is_checked = is_checked


    def create(self):
        """Save the checklist item to the database."""
        db.session.add(self)
        db.session.commit()


    def read(self):
        """Convert the checklist item object to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "item_name": self.item_name,
            "is_checked": self.is_checked,
            "timestamp": self.timestamp.isoformat()
        }


    def update(self):
        """Update the checklist item in the database."""
        db.session.add(self)  # Mark as modified
        db.session.commit()


    def delete(self):
        """Delete the checklist item from the database."""
        db.session.delete(self)
        db.session.commit()


# Function to initialize some sample data
def initChecklist():
    sample_items = [
        {"user_id": 1, "item_name": "Tent"},
        {"user_id": 1, "item_name": "Flashlight"},
        {"user_id": 2, "item_name": "Sleeping Bag"},
        {"user_id": 2, "item_name": "Camping Stove"},
    ]
    for data in sample_items:
        item = ChecklistItem(user_id=data["user_id"], item_name=data["item_name"])
        db.session.add(item)
    db.session.commit()
