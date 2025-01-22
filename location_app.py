from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize the app
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')

# Set up database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///frostbyte_table.db'  # Use frostbyte_table.db as the database
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