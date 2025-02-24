import requests
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from api.jwt_authorize import token_required

# This Blueprint object is used to define APIs for the weather service.
weather_api = Blueprint('weather_api', __name__, url_prefix='/api/weather')

# The Api object is connected to the Blueprint object to define the API endpoints.
api = Api(weather_api)

# Weather API setup
API_KEY = '9bb9d39671474da4b83164647252402'
BASE_URL = 'http://api.weatherapi.com/v1/current.json'

def fetch_coordinates(city):
    """Fetch latitude and longitude of the city using the weatherapi.com geocoding feature"""
    response = requests.get(BASE_URL, params={
        'key': API_KEY,
        'q': city,
        'aqi': 'no'
    })
    
    if response.status_code == 200:
        data = response.json()
        lat = data['location']['lat']
        lon = data['location']['lon']
        return lat, lon
    return None

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
            'pressure': data['current']['pressure_mb'],
            'wind_speed': data['current']['wind_kph']
        }
    return None

class WeatherAPI(Resource):
    """Weather API resource class"""
    @token_required()
    def get(self, city):
        """Fetch weather for a specific city."""
        city = city.strip().lower()

        # Fetch coordinates using the city name
        coordinates = fetch_coordinates(city)
        
        if not coordinates:
            return jsonify({"error": "Location not found."}), 404
        
        lat, lon = coordinates
        weather_data = fetch_weather(lat, lon)

        if weather_data:
            return jsonify({
                "location": city.replace("-", " ").title(),
                "temperature": weather_data["temperature"],
                "description": weather_data["description"],
                "humidity": weather_data["humidity"],
                "pressure": weather_data["pressure"],
                "wind_speed": weather_data["wind_speed"]
            })

        return jsonify({"error": "Unable to fetch weather data."}), 500

# Add the WeatherAPI resource to the API with the dynamic city parameter.
api.add_resource(WeatherAPI, '/<string:city>')

