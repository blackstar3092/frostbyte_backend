from flask import Blueprint, request, jsonify

location_bp = Blueprint('location', __name__)

locations = []

@location_bp.route('/api/save-location', methods=['POST'])
def save_location():
    data = request.get_json()

    lat = data.get('lat')
    lng = data.get('lng')

    if lat is None or lng is None:
        return jsonify({"error": "Invalid data"}), 400

    locations.append({"lat": lat, "lng": lng})

    return jsonify({"message": "Location saved successfully!"}), 200
