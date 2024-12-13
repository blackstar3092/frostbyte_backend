import jwt
from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.quiz_score import QuizScore

# Define the Blueprint for the Quiz API
points_api = Blueprint('points_api', __name__, url_prefix='/api')

# Connect the Api object to the Blueprint
api = Api(points_api)

class PointsAPI:
    """
    Define the API CRUD endpoints for storing quiz results.
    """

    class _CRUD(Resource):
        @token_required()
        def post(self):
            """
            Store the quiz score for the user.
            """
            current_user = g.current_user
            data = request.get_json()

            # Validate required fields
            if not data or 'points' not in data:
                return {'message': 'Points are required'}, 400

            points = data['points']
            park = data.get('park', 'Unknown')

            # Check if a quiz result already exists for the user
            existing_score = QuizScore.query.filter_by(user_id=current_user.id).first()
            if existing_score:
                # Update the existing score
                existing_score.points = points
                existing_score.park = park
                existing_score.update()
                return jsonify(existing_score.read())

            # Create a new quiz result
            new_score = QuizScore(user_id=current_user.id, points=points, park=park)
            new_score.create()
            return jsonify(new_score.read())

        @token_required()
        def get(self):
            """
            Retrieve the user's quiz score.
            """
            current_user = g.current_user
            score = QuizScore.query.filter_by(user_id=current_user.id).first()

            if not score:
                return {'message': 'Quiz result not found'}, 404

            return jsonify(score.read())

    class _ALL_SCORES(Resource):
        def get(self):
            """
            Retrieve all stored quiz scores (admin endpoint).
            """
            scores = QuizScore.query.all()
            results = [score.read() for score in scores]
            return jsonify(results)

# Map endpoints to the API
api.add_resource(PointsAPI._CRUD, '/quiz')
api.add_resource(PointsAPI._ALL_SCORES, '/quizzes')

# How to Test:
# 1. Run the Flask server.
# 2. Use Postman or a similar tool to send POST requests to '/api/quiz' with JSON payloads like:
#    {
#        "points": 150,
#        "park": "Grand Canyon National Park"
#    }
# 3. Send GET requests to '/api/quiz' to verify stored results.
