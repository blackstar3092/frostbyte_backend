import jwt
from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.quiz_result import QuizResult

# Define the Blueprint for the Quiz API
quiz_api = Blueprint('quiz_api', __name__, url_prefix='/api')

# Connect the Api object to the Blueprint
api = Api(quiz_api)

class QuizAPI:
    """
    Define the API CRUD endpoints for Quiz Result management.
    """
    
    class _Submit(Resource):
        @token_required()
        def post(self):
            """
            Submit quiz points and calculate the matching park.
            """
            current_user = g.current_user
            data = request.get_json()

            if not data or 'points' not in data:
                return {'message': 'Points are required.'}, 400

            points = data['points']

            # Determine the matching national park
            if 70 <= points <= 130:
                park = "Denali National Park"
            elif 140 <= points <= 170:
                park = "Grand Canyon National Park"
            elif 180 <= points <= 220:
                park = "Redwood National Park"
            elif 230 <= points <= 280:
                park = "Buck Island Reef National Monument"
            else:
                return {'message': 'Points out of range.'}, 400

            # Check if the user already has a quiz result
            existing_result = QuizResult.query.filter_by(user_id=current_user.id).first()
            if existing_result:
                existing_result.points = points
                existing_result.park = park
                existing_result.update()
                return jsonify(existing_result.read())

            # Create a new quiz result
            new_result = QuizResult(user_id=current_user.id, points=points, park=park)
            new_result.create()
            return jsonify(new_result.read())

    class _GetResult(Resource):
        @token_required()
        def get(self):
            """
            Retrieve the user's quiz result.
            """
            current_user = g.current_user
            result = QuizResult.query.filter_by(user_id=current_user.id).first()

            if not result:
                return {'message': 'No quiz result found.'}, 404

            return jsonify(result.read())

# Map API endpoints
api.add_resource(QuizAPI._Submit, '/points/submit')
api.add_resource(QuizAPI._GetResult, '/points/get')

# How to Test:
# 1. Run the Flask server.
# 2. Use Postman to send POST requests to '/api/points/submit' with payload:
#    {
#        "points": 185
#    }
# 3. Send GET requests to '/api/points/get' to retrieve the stored quiz result.
