from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize the Flask app
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')

# Set up the database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///locations.db'  # Using SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking (optional)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Location model (your database table)
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    lat = db.Column(db.Float, nullable=False)  # Latitude of the location
    lng = db.Column(db.Float, nullable=False)  # Longitude of the location

    def __repr__(self):
        return f"<Location {self.id}, {self.lat}, {self.lng}>"

# Route to save a location (POST request)
@app.route('/api/save-location', methods=['POST'])
def save_location():
    # Get JSON data from the request
    data = request.get_json()

    # Extract latitude and longitude from the data
    lat = data.get('lat')
    lng = data.get('lng')

    # Check if lat and lng are provided
    if lat is None or lng is None:
        return jsonify({"error": "Invalid data, lat and lng are required"}), 400

    # Create a new Location object and add it to the database
    new_location = Location(lat=lat, lng=lng)
    db.session.add(new_location)
    db.session.commit()

    return jsonify({"message": "Location saved successfully!"}), 200

# Route to get all locations (GET request)
@app.route('/api/get-locations', methods=['GET'])
def get_locations():
    # Query all locations from the database
    locations = Location.query.all()
    
    # Format locations into a list of dictionaries
    locations_list = [{"id": loc.id, "lat": loc.lat, "lng": loc.lng} for loc in locations]

    return jsonify({"locations": locations_list}), 200

# Initialize database tables before the first request
@app.before_first_request
def before_first_request():
    # Create tables for models defined (if not already created)
    db.create_all()
    print("Location tables initialized.")

if __name__ == '__main__':
    # Run the Flask app
    app.run(port=5002)  # Run on a different port if your existing app is already running on 5001
