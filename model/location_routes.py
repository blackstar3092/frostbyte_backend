import json
from flask import Blueprint, request, jsonify
import pdb  # Import the pdb module for debugging

location_bp = Blueprint('location', __name__)

def read_locations():
    try:
        with open('locations.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def write_locations(locations):
    with open('locations.json', 'w') as f:
        json.dump(locations, f)

locations = read_locations()

@location_bp.route('/api/save-location', methods=['POST'])
def save_location():
    pdb.set_trace()  # Breakpoint 1
    data = request.get_json()

    lat = data.get('lat')
    lng = data.get('lng')

    if lat is None or lng is None:
        return jsonify({"error": "Invalid data"}), 400

    locations.append({"lat": lat, "lng": lng})
    write_locations(locations)  

    pdb.set_trace()  # Breakpoint 2
    return jsonify({"message": "Location saved successfully!"}), 200

@location_bp.route('/api/get-locations', methods=['GET'])
def get_locations():
    pdb.set_trace()  # Breakpoint 3
    return jsonify({"locations": locations}), 200
