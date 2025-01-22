from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize the app
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')

# Set up database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///locations.db'  # Using SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable warnings

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Location model (for the database table)
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Location {self.id}, {self.lat}, {self.lng}>"

# Route to save a location (POST request)
@app.route('/api/save-location', methods=['POST'])
def save_location():
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
@app.route('/api/get-locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    locations_list = [{"id": loc.id, "lat": loc.lat, "lng": loc.lng} for loc in locations]

    return jsonify({"locations": locations_list}), 200

# Initialize database tables manually
def initialize_database():
    with app.app_context():
        db.create_all()  # Create the tables in the database
        print("Location tables initialized.")

if __name__ == '__main__':
    initialize_database()  # Initialize the tables before starting the app
    app.run(port=5002)  # Run the app
