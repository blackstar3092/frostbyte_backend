# models/weather.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship
from __init__ import db
from model.frostbyte import Frostbyte

class Weather(db.Model):
    __tablename__ = 'weather'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Fields related to weather
    temperature = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    humidity = db.Column(db.Integer, nullable=False)
    pressure = db.Column(db.Integer, nullable=False)

    # Foreign key for park relationship
    park_id = db.Column(db.Integer, db.ForeignKey('parks.id'), nullable=False)

    # Relationship with the Park model (assuming parks model exists)
    park = db.relationship('Park', backref=db.backref('weather', lazy=True))

    def __init__(self, temperature, description, humidity, pressure, park_id):
        self.temperature = temperature
        self.description = description
        self.humidity = humidity
        self.pressure = pressure
        self.park_id = park_id

    def create(self):
        """Create and save a new Weather entry."""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Update an existing Weather entry."""
        db.session.commit()

    def delete(self):
        """Delete an existing Weather entry."""
        db.session.delete(self)
        db.session.commit()

    def read(self):
        """Return weather data as a dictionary."""
        return {
            'id': self.id,
            'temperature': self.temperature,
            'description': self.description,
            'humidity': self.humidity,
            'pressure': self.pressure,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'park_id': self.park_id
        }
