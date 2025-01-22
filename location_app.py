# location_app.py
from flask import Flask
from flask_cors import CORS
from db import db  # Import db from the new db.py file

# Initialize the app
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')

# Set up database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///locations.db'  # Correct path for your database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable warnings

# Initialize SQLAlchemy with the app
db.init_app(app)

# Import blueprints
from api.location import location_api  # Make sure this import is correct

# Register blueprints
app.register_blueprint(location_api)

# Run the app
if __name__ == '__main__':
    app.run(port=5002)
