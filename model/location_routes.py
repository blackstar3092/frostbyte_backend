from flask import Blueprint, request, jsonify

location_bp = Blueprint('location', __name__)

locations = []

@location_bp.route('http://127.0.0.1:4887/frostbyte_frontend/api/save-location', methods=['POST'])
def save_location():
    data = request.get_json()

    lat = data.get('lat')
    lng = data.get('lng')

    if lat is None or lng is None:
        return jsonify({"error": "Invalid data"}), 400

    locations.append({"lat": lat, "lng": lng})

    return jsonify({"message": "Location saved successfully!"}), 200

@location_bp.route('http://127.0.0.1:4887/frostbyte_frontend/api/get-locations', methods=['GET'])
def get_locations():
    return jsonify({"locations": locations}), 200
