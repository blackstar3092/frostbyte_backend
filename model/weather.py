from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship
from __init__ import db

class Weather(db.Model):
    __tablename__ = 'weather'

    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Integer, nullable=False)
    humidity = db.Column(db.Integer, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    location = relationship("Location", back_populates="weather_reports")

    def __init__(self, temperature, humidity, location_id):
        self.temperature = temperature
        self.humidity = humidity
        self.location_id = location_id

    def create(self):
        db.session.add(self)
        db.session.commit()
        
    def read(self):
        return {
            self.id,
            self.temperature,
            self.humidity,
            self.location_id,
            self.timestamp.isoformat()
        }

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()