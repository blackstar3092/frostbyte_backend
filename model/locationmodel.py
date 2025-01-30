from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship
from __init__ import db

class Location(db.Model):
    __tablename__ = 'locations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('frostbytes.id'), nullable=False)    
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)  
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = relationship('Frostbyte')
    channel = relationship('Channel', back_populates='channel_locations')

    # Add unique constraint for user_id and channel_id combination
    __table_args__ = (db.UniqueConstraint('user_id', 'channel_id', name='unique_user_channel_location'),)

    def __init__(self, user_id, channel_id, latitude, longitude):
        self.user_id = user_id
        self.channel_id = channel_id
        self.latitude = latitude
        self.longitude = longitude

    def create(self):
        """Save the location to the database."""
        db.session.add(self)
        db.session.commit()

    def read(self):
        """Convert the location object to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "channel_id": self.channel_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
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

def initLocations():
    """Initialize the locations with sample data."""
    sample_locations = [
        {"user_id": 1, "channel_id": 10, "latitude": 37.7749, "longitude": -122.4194},
        {"user_id": 2, "channel_id": 11, "latitude": 40.7128, "longitude": -74.0060},
        {"user_id": 3, "channel_id": 12, "latitude": 34.0522, "longitude": -118.2437},
    ]
    for data in sample_locations:
        location = Location(
            user_id=data["user_id"], 
            channel_id=data["channel_id"], 
            latitude=data["latitude"], 
            longitude=data["longitude"]
        )
        db.session.add(location)
    db.session.commit()
