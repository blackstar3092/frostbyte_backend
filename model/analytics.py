from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship
from model.post import Post
from __init__ import db

class Analytics(db.Model):
    __tablename__ = 'analytics'

    id = db.Column(db.Integer, primary_key=True)  # Primary key for the analytics table
    park_id = db.Column(db.String(50), nullable=False)  # ID of the park being analyzed
    stars = db.Column(db.Float, nullable=False)  # Average star rating
    total_reviews = db.Column(db.Integer, nullable=False)  # Total number of reviews
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for creation
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)  # Timestamp for updates


    def __init__(self, park_id, stars, total_reviews):
        """
        Initialize the Analytics model with the given data.
        """
        self.park_id = park_id
        self.stars = stars
        self.total_reviews = total_reviews

    def create(self):
        """
        Save the analytics entry to the database.
        """
        db.session.add(self)
        db.session.commit()

    def read(self):
        """
        Serialize the model data into a dictionary for JSON serialization.
        """
        return {
            'id': self.id,
            'park_id': self.park_id,
            'stars': self.stars,
            'total_reviews': self.total_reviews,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def update(self):
        """
        Commit changes to the database for the current instance.
        """
        db.session.commit()

    def delete(self):
        """
        Delete the analytics entry from the database.
        """
        db.session.delete(self)
        db.session.commit()
        

