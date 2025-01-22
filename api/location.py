from flask import Blueprint, request, jsonify

# Define your blueprint for handling location-related requests
location_api = Blueprint('location', __name__)

# Route to save a location (POST request)
@location_api.route('/api/save-location', methods=['POST'])
def save_location():
    # Get the latitude and longitude from the request data
    data = request.get_json()
    lat = data.get('lat')
    lng = data.get('lng')

    if lat is None or lng is None:
        return jsonify({"error": "Invalid data, lat and lng are required"}), 400

    # Create a new Location object and add it to the database
    new_location = Location(lat=lat, lng=lng)
    db.session.add(new_location)
    db.session.commit()

    return jsonify({"message": "Location saved successfully!"}), 200

# Route to get all locations (GET request)
@location_api.route('/api/get-locations', methods=['GET'])
def get_locations():
    # Query the database for all locations
    locations = Location.query.all()
    locations_list = [{"id": loc.id, "lat": loc.lat, "lng": loc.lng} for loc in locations]

    return jsonify({"locations": locations_list}), 200
