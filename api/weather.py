import requests
from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required

# This Blueprint object is used to define APIs for the weather service.
weather_api = Blueprint('weather_api', __name__, url_prefix='/api/weather')

# The Api object is connected to the Blueprint object to define the API endpoints.
api = Api(weather_api)

# Weather API setup
API_KEY = '9bb9d39671474da4b83164647252402'
BASE_URL = 'http://api.weatherapi.com/v1/current.json'

# Locations dictionary for predefined places
LOCATIONS = {
    "grand-canyon": {"lat": 36.1069, "lon": -112.1129},
    "denali": {"lat": 63.4348, "lon": -148.2670},
    "redwood": {"lat": 41.2132, "lon": -124.0046},
    "buck-reef": {"lat": 29.6074, "lon": -81.3886}  # Example coordinates
}

@token_required()
def fetch_weather(lat, lon):
    """Fetch weather information from the weatherapi.com"""
    response = requests.get(BASE_URL, params={
        'key': API_KEY,
        'q': f'{lat},{lon}',
        'aqi': 'no'
    })

    if response.status_code == 200:
        data = response.json()
        return {
            'temperature': data['current']['temp_c'],
            'description': data['current']['condition']['text'],
            'humidity': data['current']['humidity'],
            'pressure': data['current']['pressure_mb']
        }
    return None

class WeatherAPI(Resource):
    """Weather API resource class"""
    @token_required()
    def get(self, location):
        """Fetch weather for a specific location."""
        location = location.lower()

        if location not in LOCATIONS:
            return jsonify({"error": "Location not found."}), 404

        lat, lon = LOCATIONS[location]["lat"], LOCATIONS[location]["lon"]
        weather_data = fetch_weather(lat, lon)

        if weather_data:
            return jsonify({
                "location": location.replace("-", " ").title(),
                "temperature": weather_data["temperature"],
                "description": weather_data["description"],
                "humidity": weather_data["humidity"],
                "pressure": weather_data["pressure"]
            })

        return jsonify({"error": "Unable to fetch weather data."}), 500

# Add the WeatherAPI resource to the API with the dynamic location parameter.
api.add_resource(WeatherAPI, '/<string:location>')

