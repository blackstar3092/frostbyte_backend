from app import app  # Import your Flask app from app.py
from model.location_routes import location_bp  # Import the location blueprint from location_routes.py

# Register the blueprint in a separate script
app.register_blueprint(location_bp)

if __name__ == '__main__':
    app.run(debug=True)