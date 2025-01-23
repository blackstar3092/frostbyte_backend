from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship
#from model.post import Post
from __init__ import db
from api.jwt_authorize import token_required


class Rating(db.Model):
    __tablename__ = 'ratings'
    
    id = db.Column(db.Integer, primary_key=True)
    stars = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('frostbytes.id'), nullable=False)    
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = relationship('Frostbyte')
    channel = relationship('Channel', back_populates='channel_ratings')

    # Add unique constraint for user_id and channel_id combination
    __table_args__ = (db.UniqueConstraint('user_id', 'channel_id', name='unique_user_channel_rating'),)

    
    def __init__(self, stars, user_id, channel_id):
        self.stars = stars
        self.user_id = user_id
        self.channel_id = channel_id

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
            "channel_id": self.channel_id,
            "timestamp": self.timestamp.isoformat()
        }

    def update(self):
        """Update the rating in the database."""
        db.session.add(self)  # Explicitly add it to the session (mark it as modified)
        db.session.commit()


    def delete(self):
        """Delete the rating from the database."""
        db.session.delete(self)
        db.session.commit()

    
def initRatings():
    from model.rating import Rating  # Import inside the function to avoid circular imports
    sample_ratings = [
        {"stars": 5, "user_id": 1, "channel_id": 10},
        {"stars": 4, "user_id": 2, "channel_id": 11},
        {"stars": 3, "user_id": 3, "channel_id": 12},
    ]
    for data in sample_ratings:
        rating = Rating(stars=data["stars"], user_id=data["user_id"], channel_id=data["channel_id"])
        db.session.add(rating)
    db.session.commit()