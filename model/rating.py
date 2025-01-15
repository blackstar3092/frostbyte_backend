from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship
from model.post import Post
from __init__ import db

class Rating(db.Model):
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    stars = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


    post = relationship("Post", back_populates="ratings")

    def __init__(self, stars, user_id, post_id):
        self.stars = stars
        self.user_id = user_id
        self.post_id = post_id

    def create(self):
        """Save the rating to the database."""
        db.session.add(self)
        db.session.commit()
        
    def read(self):
        """Convert the rating object to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "stars": self.stars,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "timestamp": self.timestamp.isoformat()
        }

    def update(self):
        """Update the rating in the database."""
        db.session.commit()

    def delete(self):
        """Delete the rating from the database."""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def initialize_sample_data_ratings():
        """Static method to initialize the ratings table with sample data."""
        sample_ratings = [
            {"stars": 5, "user_id": 1, "post_id": 1},
            {"stars": 4, "user_id": 2, "post_id": 2},
            {"stars": 3, "user_id": 3, "post_id": 3},
        ]
        for data in sample_ratings:
            rating = Rating(stars=data["stars"], user_id=data["user_id"], post_id=data["post_id"])
            db.session.add(rating)
        db.session.commit()
    