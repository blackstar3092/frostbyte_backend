from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship
from __init__ import db
from api.jwt_authorize import token_required

class Location(db.Model):
    __tablename__ = 'locations'
    
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Integer, nullable=False)
    lng = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('frostbytes.id'), nullable=False)    
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship('Frostbyte', backref='locations')  # Access locations from the user model
    channel = relationship('Channel', back_populates='channel_locations')  # Access locations from the channel model

    # Optional: Add unique constraint for user_id and channel_id combination
    __table_args__ = (db.UniqueConstraint('user_id', 'channel_id', name='unique_user_channel_locations'),)

    def __init__(self, lat, lng, user_id, channel_id):
        self.lat = lat
        self.lng = lng
        self.user_id = user_id
        self.channel_id = channel_id

    def create(self):
        """Save the location to the database."""
        db.session.add(self)
        db.session.commit()

    def read(self):
        """Convert the location object to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "lat": self.lat,
            "lng": self.lng,
            "user_id": self.user_id,
            "channel_id": self.channel_id,
            "timestamp": self.timestamp.isoformat()
        }

    def update(self):
        """Update the location in the database."""
        db.session.add(self)  # Explicitly add it to the session (mark it as modified)
        db.session.commit()

    def delete(self):
        """Delete the location from the database."""
        db.session.delete(self)
        db.session.commit()


def initLocation():
    from model.locationmodel import Location  # Import inside the function to avoid circular imports
    sample_locations = [
        {"lat": 36.06173, "lng": -112.10775, "user_id": 2, "channel_id": 13},
        {"lat": 17.74401, "lng": -64.62177, "user_id": 3, "channel_id": 11},
        {"lat": 36.08888, "lng": -112.20793, "user_id": 3, "channel_id": 11},
    ]
    for data in sample_locations:
        location = Location(lat=data["lat"], lng=data["lng"], user_id=data["user_id"], channel_id=data["channel_id"])
        db.session.add(location)
    db.session.commit()
