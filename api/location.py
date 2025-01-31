import jwt
from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from datetime import datetime
from __init__ import app
from model.locationmodel import Location

# Define the Blueprint for the Location API
location_api = Blueprint('location_api', __name__, url_prefix='/api')

# Connect the Api object to the Blueprint
api = Api(location_api)

class LocationAPI:
    """
    Define the API CRUD endpoints for storing and retrieving user locations.
    """

    class _CRUD(Resource):
        def post(self):
            """
            Store or update the user's location.
            """
            current_user = g.current_user
            data = request.get_json()

            # Validate required fields
            if not data or 'latitude' not in data or 'longitude' not in data:
                return {'message': 'Latitude and Longitude are required'}, 400

            latitude = data['latitude']
            longitude = data['longitude']

            # Check if a location entry already exists for the user
            existing_location = Location.query.filter_by(user_id=current_user.id).first()
            if existing_location:
                # Update the existing location
                existing_location.latitude = latitude
                existing_location.longitude = longitude
                existing_location.update()
                return jsonify(existing_location.read())

            # Create a new location entry
            new_location = Location(user_id=current_user.id, latitude=latitude, longitude=longitude)
            new_location.create()
            return jsonify(new_location.read())

        def get(self):
            """
            Retrieve the user's last known location.
            """
            current_user = g.current_user
            location = Location.query.filter_by(user_id=current_user.id).first()

            if not location:
                return {'message': 'Location not found'}, 404

            return jsonify(location.read())

    class _ALL_LOCATIONS(Resource):
        def get(self):
            """
            Retrieve all stored locations (admin endpoint).
            """
            locations = Location.query.all()
            results = [location.read() for location in locations]
            return jsonify(results)

# Map endpoints to the API
api.add_resource(LocationAPI._CRUD, '/location')
api.add_resource(LocationAPI._ALL_LOCATIONS, '/locations')
