import json
from flask import Blueprint, request, jsonify
from app import db  # Import db object from app.py
from sqlalchemy import Integer, String

# Define the blueprint
location_bp = Blueprint('location', __name__)

# Define the Location model
class Location(db.Model):
    id = db.Column(Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Location {self.id}, {self.lat}, {self.lng}>"

# Route to save a location
@location_bp.route('/api/save-location', methods=['POST'])
def save_location():
    data = request.get_json()

    lat = data.get('lat')
    lng = data.get('lng')

    if lat is None or lng is None:
        return jsonify({"error": "Invalid data"}), 400

    # Create a new Location object and add to the database
    new_location = Location(lat=lat, lng=lng)
    db.session.add(new_location)
    db.session.commit()

    return jsonify({"message": "Location saved successfully!"}), 200

# Route to get all locations
@location_bp.route('/api/get-locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()  # Get all locations from the database
    locations_list = [{"id": loc.id, "lat": loc.lat, "lng": loc.lng} for loc in locations]

    return jsonify({"locations": locations_list}), 200
