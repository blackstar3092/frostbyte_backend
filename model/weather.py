from __init__ import db
from datetime import datetime

class Weather(db.Model):
    __tablename__ = 'weather'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Fields related to weather
    temperature = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    humidity = db.Column(db.Integer, nullable=False)
    pressure = db.Column(db.Integer, nullable=False)
    
    # A foreign key to associate this weather data with a specific park
    park_id = db.Column(db.Integer, db.ForeignKey('parks.id'), nullable=False)

    # Relationship to the park model (assuming you have a parks table)
    park = db.relationship('Park', backref=db.backref('weather', lazy=True))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, temperature, description, humidity, pressure, park_id):
        self.temperature = temperature
        self.description = description
        self.humidity = humidity
        self.pressure = pressure
        self.park_id = park_id

    def create(self):
        """Method to create and insert a new Weather entry."""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Method to update an existing Weather entry."""
        db.session.commit()

    def delete(self):
        """Method to delete an existing Weather entry."""
        db.session.delete(self)
        db.session.commit()

    def read(self):
        """Return the weather data as a dictionary."""
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
