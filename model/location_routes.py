import json
from flask import Blueprint, request, jsonify

location_bp = Blueprint('location', __name__)

# Read the saved locations from a file on app start
def read_locations():
    try:
        with open('locations.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Write locations to the file
def write_locations(locations):
    with open('locations.json', 'w') as f:
        json.dump(locations, f)

# Retrieve locations from the file
locations = read_locations()

@location_bp.route('/api/save-location', methods=['POST'])
def save_location():
    data = request.get_json()

    lat = data.get('lat')
    lng = data.get('lng')

    if lat is None or lng is None:
        return jsonify({"error": "Invalid data"}), 400

    locations.append({"lat": lat, "lng": lng})
    write_locations(locations)  # Save the updated locations to the file

    return jsonify({"message": "Location saved successfully!"}), 200

@location_bp.route('/api/get-locations', methods=['GET'])
def get_locations():
    return jsonify({"locations": locations}), 200
