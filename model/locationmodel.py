# model/locationmodel.py
from db import db  # Import db from db.py

# Define a Location model
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Location {self.id}, {self.lat}, {self.lng}>"
