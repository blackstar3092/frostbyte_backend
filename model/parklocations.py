from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from __init__ import db

class ParkLocation(db.Model):
    __tablename__ = 'parklocations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, name, description, latitude, longitude):
        self.name = name
        self.description = description
        self.latitude = latitude
        self.longitude = longitude

    def create(self):
        db.session.add(self)
        db.session.commit()
        
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timestamp": self.timestamp.isoformat()
        }

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def initialize_sample_data_parklocations():
        sample_locations = [
            {"name": "Grand Canyon South Rim", "description": "The most popular and easily accessible part of the Grand Canyon.", "latitude": 36.1069, "longitude": -112.1129},
            {"name": "Grand Canyon North Rim", "description": "Less visited and more remote part of the Grand Canyon.", "latitude": 36.2545, "longitude": -112.1325},
            {"name": "Grand Canyon West Rim", "description": "Home to the Skywalk, a glass bridge over the canyon.", "latitude": 36.0980, "longitude": -113.5353},
            {"name": "Havasu Falls", "description": "A stunning waterfall located in the Havasupai Indian Reservation.", "latitude": 36.2340, "longitude": -112.7421},
            {"name": "Desert View Watchtower", "description": "An iconic stone tower offering panoramic views of the canyon.", "latitude": 36.0290, "longitude": -112.0245}
        ]
        for loc in sample_locations:
            location = ParkLocation(name=loc["name"], description=loc["description"], latitude=loc["latitude"], longitude=loc["longitude"])
            db.session.add(location)
        db.session.commit()

def initialize_sample_parklocations():
    ParkLocation.initialize_sample_data_parklocations()
