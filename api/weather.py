from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import requests

# Create a blueprint for the weather API
weather_api = Blueprint('weather_api', __name__, url_prefix='/api')
# Create an Api object and associate it with the Blueprint
api = Api(weather_api)

# Open-Meteo API base URL
OPEN_METEO_BASE_URL = "https://api.open-meteo.com/v1/forecast"

class Weather(Resource):
    """
    Weather API to fetch current weather and forecast details for a given location.
    """

    @staticmethod
    def get_coordinates(location):
        """
        Mock function to return hardcoded latitude and longitude for a location.
        Replace this with a geocoding API for real-world scenarios.
        """
        location_coords = {
            "San Diego": (32.7157, -117.1611),
            "Los Angeles": (34.0522, -118.2437),
            "New York": (40.7128, -74.0060),
            "Denver": (39.7392, -104.9903),
        }
        return location_coords.get(location, None)

    def get(self):
        """
        Fetch weather data based on location.
        Request query parameters:
        - location: The name of the location (e.g., San Diego).
        - type: 'current' for current weather, 'forecast' for multi-day forecast.
        """
        try:
            # Extract query parameters
            location = request.args.get('location', 'San Diego')  # Default to San Diego
            weather_type = request.args.get('type', 'forecast').lower()  # Default to forecast

            # Validate location
            if not location:
                return jsonify({"error": "Location is required."}), 400

            # Get coordinates for the location
            coordinates = self.get_coordinates(location)
            if not coordinates:
                return jsonify({"error": f"Location '{location}' not found. Please use a valid location."}), 404

            latitude, longitude = coordinates

            # Prepare Open-Meteo API request parameters
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": True,
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode",
                "timezone": "auto",
            }

            # Make the API request
            response = requests.get(OPEN_METEO_BASE_URL, params=params)

            if response.status_code != 200:
                return jsonify({"error": "Failed to fetch weather data."}), response.status_code

            weather_data = response.json()

            # Process and return data based on the type requested
            if weather_type == 'current':
                current_weather = weather_data.get("current_weather", {})
                return jsonify({
                    "location": location,
                    "latitude": latitude,
                    "longitude": longitude,
                    "current_weather": current_weather
                })
            elif weather_type == 'forecast':
                daily_forecast = weather_data.get("daily", {})
                return jsonify({
                    "location": location,
                    "latitude": latitude,
                    "longitude": longitude,
                    "daily_forecast": daily_forecast
                })
            else:
                return jsonify({"error": "Invalid type. Use 'current' or 'forecast'."}), 400

        except Exception as e:
            import traceback
            print(f"Error occurred: {str(e)}")
            traceback.print_exc()  # Log the full traceback
            return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500

# Add the resource to the API
api.add_resource(Weather, '/weather')
