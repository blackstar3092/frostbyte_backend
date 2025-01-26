import jwt
from flask import Blueprint, request, jsonify, current_app, g
from flask_restful import Api, Resource
from datetime import datetime
from __init__ import app, db
from api.jwt_authorize import token_required

# Delayed imports inside the function to avoid circular imports
def initLocation():
    from model.locationmodel import Location  # Import inside the function to avoid circular imports
    from model.frostbyte import Frostbyte    # Import inside the function to avoid circular imports
    from model.channel import Channel

# Blueprint for Location API
location_api = Blueprint('location_api', __name__, url_prefix='/api')
api = Api(location_api)

class LocationAPI:
    class _CRUD(Resource):
        @token_required
        def post(self):
            """Create a new location."""
            current_user = g.current_user  # Get the currently logged-in user
            data = request.get_json()

            if not data or 'lat' not in data or 'lng' not in data or 'user_id' not in data:
                return {'message': 'Missing required fields (lat, lng, user_id)'}, 400

            # Create the new location record
            location = location(lat=data['lat'], lng=data['lng'], user_id=data['user_id'], channel_id=data.get('channel_id'))
            location.create()

            return jsonify(location.read()), 201  # Return the created location as JSON

        @token_required
        def get(self):
            """Fetch all locations."""
            locations = locations.query.all()
            if not locations:
                return {'message': 'No locations found'}, 404

            return jsonify([location.read() for location in locations]), 200

    class _LOCATION(Resource):
        @token_required
        def post(self):
            """Handle both creating and fetching a location."""
            current_user = g.current_user
            data = request.get_json()

            # If lat/lng are passed, handle storing a new location
            if 'lat' in data and 'lng' in data:
                if not data or 'lat' not in data or 'lng' not in data or 'user_id' not in data:
                    return {'message': 'Missing required fields (lat, lng, user_id)'}, 400

                # Create or update the location
                location = location.query.filter_by(user_id=current_user.id, channel_id=data.get('channel_id')).first()
                if location:
                    location.lat = data['lat']
                    location.lng = data['lng']
                    location.timestamp = datetime.utcnow()  # Optionally update the timestamp
                else:
                    location = location(lat=data['lat'], lng=data['lng'], user_id=current_user.id, channel_id=data.get('channel_id'))
                    db.session.add(location)
                db.session.commit()
                return {'message': 'Location saved successfully', 'location': location.read()}, 201

            # If lat/lng are not passed, assume it's a fetch request
            elif 'user_id' in data and 'channel_id' in data:
                user_id = data.get('user_id')
                channel_id = data.get('channel_id')

                location = location.query.filter_by(user_id=user_id, channel_id=channel_id).first()

                if not location:
                    return {'message': 'No location found for the specified user and channel'}, 404

                return jsonify(location.read()), 200

            return {'message': 'Invalid request'}, 400

    class _LOCATION_ID(Resource):
        @token_required
        def get(self, location_id):
            """Retrieve a single location by ID."""
            location = location.query.get(location_id)
            if not location:
                return {'message': 'Location not found'}, 404

            return jsonify(location.read()), 200

        @token_required
        def delete(self, location_id):
            """Delete a location by ID."""
            location =location.query.get(location_id)
            if not location:
                return {'message': 'Location not found'}, 404

            db.session.delete(location)
            db.session.commit()
            return {'message': f'Location {location_id} deleted successfully'}, 200

    # Map resources to endpoints
    api.add_resource(_CRUD, '/locations')  # Handles create and list all locations
    api.add_resource(_LOCATION, '/location')  # Handles storing and fetching a location
    api.add_resource(_LOCATION_ID, '/location/<int:location_id>')  # Handles get and delete a specific location