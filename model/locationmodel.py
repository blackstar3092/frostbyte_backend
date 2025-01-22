from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from model.locationmodel import db, Location

# Initialize the Flask app
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')

# Set up the database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///locations.db'  # Using SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking (optional)

# Initialize SQLAlchemy
db.init_app(app)

# Route to save a location (POST request)
@app.route('/api/save-location', methods=['POST'])
def save_location():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    lat = data.get('lat')
    lng = data.get('lng')

    if name is None or description is None or lat is None or lng is None:
        return jsonify({"error": "Invalid data, all fields are required"}), 400

    # Create a new Location object and add it to the database
    new_location = Location(name=name, description=description, lat=lat, lng=lng)
    db.session.add(new_location)
    db.session.commit()

    return jsonify({"message": "Location saved successfully!"}), 200

# Route to get all locations (GET request)
@app.route('/api/get-locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    locations_list = [loc.to_dict() for loc in locations]
    return jsonify({"locations": locations_list}), 200

# Route to get a single location by ID (GET request)
@app.route('/api/get-location/<int:id>', methods=['GET'])
def get_location(id):
    location = Location.query.get(id)
    if location:
        return jsonify(location.to_dict()), 200
    else:
        return jsonify({"error": "Location not found"}), 404

# Route to update a location by ID (PUT request)
@app.route('/api/update-location/<int:id>', methods=['PUT'])
def update_location(id):
    location = Location.query.get(id)
    if location:
        data = request.get_json()
        location.name = data.get('name', location.name)
        location.description = data.get('description', location.description)
        location.lat = data.get('lat', location.lat)
        location.lng = data.get('lng', location.lng)

        db.session.commit()
        return jsonify({"message": "Location updated successfully!"}), 200
    else:
        return jsonify({"error": "Location not found"}), 404

# Route to delete a location by ID (DELETE request)
@app.route('/api/delete-location/<int:id>', methods=['DELETE'])
def delete_location(id):
    location = Location.query.get(id)
    if location:
        db.session.delete(location)
        db.session.commit()
        return jsonify({"message": "Location deleted successfully!"}), 200
    else:
        return jsonify({"error": "Location not found"}), 404

# Initialize database tables before the first request
@app.before_first_request
def before_first_request():
    # Create tables for models defined (if not already created)
    db.create_all()
    print("Location tables initialized.")

if __name__ == '__main__':
    app.run(port=5002)  # Run on a different port if your existing app is already running on 5001
